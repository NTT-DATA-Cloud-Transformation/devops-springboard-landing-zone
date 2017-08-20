Deploys the pipeline that will create the stacks

### Currently creating:
1. Landing zone stack - includes all the network
1. ECS cluster

### In progress:
1. IAM stack - IAM roles common across the board
1. service - Get our service into S3

### Improvemnts:
1. Rename landing zone to network
1. Currently taking the Templates bucket as a parameter. Should be moved
into the template, although name should stay a parameter
