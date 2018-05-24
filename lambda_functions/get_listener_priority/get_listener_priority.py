import boto3
import os
import botocore
import datetime
from boto3.dynamodb.conditions import Attr
import time
import cfnresponse
import json
import traceback

NO_HOLDER = '__empty__'
LOCK_ID = os.environ['StackPrefix']


def timestamp_millis():
    return int((datetime.datetime.utcnow() -
                datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


def get_empty_slot():
    elb_client = boto3.client("elbv2")
    response = elb_client.describe_rules(
        ListenerArn=os.environ['ListnerArn']
    )
    listener_priority_rules = [x['Priority'] for x in response['Rules']]
    slot = 0
    for i in range(1, 101):
        if str(i) not in listener_priority_rules:
            slot = i
            break
    return slot


def prune_expired_lock(table, priority='0'):
    now = timestamp_millis()
    try:
        table.put_item(
            Item={
                'LockId': LOCK_ID,
                'expire_ts': 0,
                'holder': NO_HOLDER,
                'priority': priority
            },
            ConditionExpression=Attr("expire_ts").lt(now) | Attr('LockId').not_exists()
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Prune: LockId={0} Prune failed".format(LOCK_ID))
            return False
    print("Prune: LockId={0}, Prune succeeded".format(LOCK_ID))
    return True


def acquire_lock(table, waitms, caller, priority):
    prune_expired_lock(table, priority)
    expire_ts = timestamp_millis() + waitms
    try:
        table.put_item(
            Item={
                'LockId': LOCK_ID,
                'expire_ts': expire_ts,
                'holder': caller,
                'priority': priority
            },
            ConditionExpression=(Attr("holder").eq(NO_HOLDER)) | Attr('LockId').not_exists()
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(
            "Write_item: LockId={0}, caller {1}, priority {2} lock is being held".format(LOCK_ID, caller, priority))
            return False
    print("Write_item: LockId={0}, caller {1}, priority {2} lock is acquired".format(LOCK_ID, caller, priority))
    return True


def has_timed_out(timestamp):
    print(timestamp_millis() - timestamp)
    return (timestamp_millis() - timestamp) > (270 * 1000)


def release_lock(table, caller):
    try:
        table.put_item(
            Item={
                'LockId': LOCK_ID,
                'expire_ts': 0,
                'holder': NO_HOLDER
            },
            ConditionExpression=Attr("holder").eq(caller) | Attr('LockId').not_exists()
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("clear_lock_item: lockname={0}, {1} release failed".format(LOCK_ID, caller))
            return False
    print("clear_lock_item: lockname={0}, {1} release succeeded".format(LOCK_ID, caller))
    return True


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    response = {}
    caller = event['ResourceProperties']['StackName']
    timestamp = timestamp_millis()
    print("Timestamp: {0}".format(timestamp))
    try:
        if event['RequestType'] == 'Delete':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, response, caller)
            return
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['DynamoDbTable'])
        caller = event['ResourceProperties']['StackName']
        locked = False
        priority = get_empty_slot()
        while (not locked):
            locked = acquire_lock(table, 30000, caller, priority)
            time.sleep(1)
            priority = get_empty_slot()
            if (has_timed_out(timestamp)):
                print("Timed out for {0}".format(caller))
                cfnresponse.send(event, context, cfnresponse.FAILED, response, caller)
                break
        if locked:
            response['priority'] = priority
            cfnresponse.send(event, context, cfnresponse.SUCCESS, response, caller)
        new_slot = get_empty_slot()
        while new_slot == priority:
            time.sleep(1)
            new_slot = get_empty_slot()
        release_lock(table, caller)
    except Exception as e:
        print(e)
        traceback.print_exc()
        cfnresponse.send(event, context, cfnresponse.FAILED, response, caller)
