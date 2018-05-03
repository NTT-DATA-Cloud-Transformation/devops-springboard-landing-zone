This template deploys the assets necessary to manage the various
templates in the ecs-wokshop-services repo. It will:
1. Create a bucket in S3
1. Deploy a CodePipeline to get the templates in the code repo into the
S3 bucket we just created.

It will use the same Stack prefix other landing zone assets use.

### S3 bucket
Proposed library and workspace bucket
```
Bucket
|-- admin
|  |-- cf-templates
|  |  |- ecs-workshop-service
|
|-- services
   |-- workspace
      |-- <service a>
      |-- <service b>

```
