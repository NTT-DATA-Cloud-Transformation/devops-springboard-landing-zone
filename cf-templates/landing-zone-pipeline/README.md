Deploys the pipeline that will create the stacks

### Currently creating:
1. IAM stack - IAM roles common across the board
1. Landing zone stack - includes all the network
1. ECS cluster
1. service - Get our service into S3

### Prerequisites
1. Deploy [git2s3](https://aws.amazon.com/about-aws/whats-new/2017/09/connect-your-git-repository-to-amazon-s3-and-aws-services-using-webhooks-and-new-quick-start/) Quickstart solution 
2. Create a keypair to launch EC2 instances where ECS cluster will be running 
