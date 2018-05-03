# Overview 

This repository contains the templates to create landing-zone resources like VPC, IAM Roles, Application loadbalancer etc


## Getting started

Deploy all the stacks here by deploying the [codepipeline.yml](cf-templates/codepipeline) cloudformation template. All the rest of the templates are deployed through this pipeline. 

The CodePipeline deploys following stacks:
1. IAM
2. Network
3. ECS Cluster
4. Service Manager Pipeline


































