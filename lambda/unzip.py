from __future__ import print_function

import boto3
import json
import os
import urllib
import zipfile

print('Loading function')

s3 = boto3.client('s3')

def get_user_params(job_data):
    """
    Args:
        job_data:
            The job data structure containing the UserParameters string which
            should contain valid JSON

    Returns:
        The JSON parameters decoded as a dictionary
    """
    try:
        user_parameters = job_data['actionConfiguration']['configuration']['UserParameters']
        decoded_parameters = json.loads(user_parameters)
    except Exception as e:
        raise Exception('UserParmeters could not be decoded as JSON')

    if 'bucket' not in decoded_parameters:
        raise Exception('Your UserParameters must include "bucket"')
    if 'key' not in decoded_parameters:
        raise Exception('Your UserParameters must include "bucket"')




def lambda_handler(event, context):

    job_id = event['CodePipeline.job']['id']
    job_data = event['CodePipeline.job']['data']
    params = get_user_params(job_data)

    bucket = event['Records'][0]['s3']['bucket']['name']
    url = event['Records'][0]['s3']['object']['key'].encode('utf8')
    key = urllib.unquote_plus(url)
    s3_path = os.path.dirname(key)
    try:
        s3.download_file(bucket, key, '/tmp/target.zip')
        zfile = zipfile.ZipFile('/tmp/target.zip')
        namelist = zfile.namelist()
        for filename in namelist:
            data = zfile.read(filename)
            localpath = '/tmp/{}'.format(str(filename))
            f = open(localpath, 'wb')
            f.write(data)
            f.close()
            s3.upload_file(localpath, bucket, os.path.join(s3_path, filename))
        s3.delete_object(Bucket=bucket, Key=key)
        return "AWS Key -> {}".format(key)
    except Exception as e:
        print(e)
        raise e
