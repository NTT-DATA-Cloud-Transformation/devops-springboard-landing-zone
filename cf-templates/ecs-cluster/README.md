
Create:
1. ECS cluster
2. ASG for ECS cluster
3. ALB for ECS cluster
4. Listener on ALB on port 80

Service templates will reference directly the exports from this template to
deploy the services.
