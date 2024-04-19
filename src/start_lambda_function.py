import boto3
import json
import os

def lambda_handler(event, context):
    bucket_name = os.environ['bucket_name']
    object_key = 'ecs_services.json'
    ecs_client = boto3.client('ecs')

    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    ecs_services = json.loads(response['Body'].read().decode('utf-8'))

    for cluster_name, service_arns in ecs_services.items():
        for service_arn in service_arns:
            ecs_client.update_service(
                cluster=cluster_name,
                service=service_arn.split('/')[-1],
                desiredCount=1
            )
            print(f"Started service {cluster_name}/{service_arn}")

    return {
        'statusCode': 200,
        'body': json.dumps('Desired counts updated for all services.')
    }
