# ecs-workshop-lz  

This repository contains the templates to create landing-zone resources like VPC, IAM Roles, Application loadbalancer etc


## Getting started

Deploy all the stacks here by deploying the [codepipeline.yml](https://github.com/sampritavh/ecs-workshop-lz/tree/master/cf-templates/codepipeline) cloudformation template. All the rest of the templates are deployed through this pipeline. 

The CodePipeline deploys following stacks:
1. iam
2. network
3. ECS Cluster
4. Service Manager


































