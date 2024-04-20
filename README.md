# ECS-TimeBased-Scheduler

Start and stop your ECS (Fargate) Services on a time based schedule.

---

In non-production environments such as QA, UAT, and DEV, ECS services may not need to run continuously. Nevertheless, manually starting and stopping these services can be time-consuming and error-prone, leading to wasted resources and increased operational overhead.

To automate the time-based running of AWS ECS (Fargate) Services, we can use AWS Lambda functions, EventBridge rules, and S3 storage. 
- The first function will stop ECS services and store their current state in an S3 bucket. 
- The second function will start ECS services based on the stored state. 
- EventBridge rules will trigger these Lambda functions at specified intervals using cron expressions to enforce the desired runtime schedules.

***Stopping ECS Services Lambda Function:*** This Lambda function is designed to run on a scheduled basis and is triggered by an EventBridge rule. Its purpose is to retrieve a list of currently running ECS services, along with their associated clusters. For each service, the function sets the desired task count to 0, effectively stopping the service. Furthermore, the function stores a record of all stopped services in an S3 bucket for future reference.

***Starting ECS Services Lambda Function:*** This Lambda function is responsible for starting ECS services based on a separate EventBridge rule. Its task is to retrieve the list of stopped services from the S3 bucket, and for each service in the list, adjust the desired task count to the desired value. This effectively restarts the service, ensuring that it is up and running.

---
![ecs_scheduler](https://github.com/senad-d/ecs-timebased-scheduler/assets/112484166/2a0800a2-61ee-470f-86de-da7dd351f317)

## Prerequisites

- `AWS IAM` - IAM User
- `S3` - S3 bucket for terraform state
- `terraform` - version 1.5.0

## Usage

```shell
terraform init -backend-config=backend/dev.tfvars
terraform apply -var-file=variables/dev.tfvars   
```

## Documentation

- [terraform](https://developer.hashicorp.com/terraform/docs)
