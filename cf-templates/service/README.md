This template deploys the assets necessary to manage the various
templates in the ecs-wokshop-services repo. It will:
1. Create an S3 bucket to use for deploying the template
2. Deploy a CodePipeline to get the templates in the code repo into the
S3 bucket we just created.

It will use the same Stack prefix other landing zone assets use.
