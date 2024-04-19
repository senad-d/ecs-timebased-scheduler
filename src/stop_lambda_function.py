import boto3
import json
import os

def lambda_handler(event, context):
    bucket_name = os.environ['bucket_name']
    object_key = 'ecs_services.json'
    ecs_client = boto3.client('ecs')
    clusters_response = ecs_client.list_clusters()
    cluster_arns = clusters_response['clusterArns']
    clusters_services = {}

    for cluster_arn in cluster_arns:
        cluster_name = cluster_arn.split('/')[-1]
        running_services = []
        next_token = None
        while True:
            list_services_params = {'cluster': cluster_arn}
            if next_token:
                list_services_params['nextToken'] = next_token

            services_response = ecs_client.list_services(**list_services_params)
            service_arns = services_response['serviceArns']

            for service_arn in service_arns:
                service_info = ecs_client.describe_services(cluster=cluster_arn, services=[service_arn])
                service_details = service_info['services'][0]

                if 'runningCount' in service_details and 'desiredCount' in service_details:
                    if service_details['desiredCount'] == 1 and service_details['runningCount'] == 1:
                        running_services.append(service_arn)
                        desired_count = service_details['desiredCount']
                        print(f"Service {cluster_name}/{service_arn} - {desired_count}")

            next_token = services_response.get('nextToken')
            if not next_token:
                break

        clusters_services[cluster_name] = running_services

        for running_service_arn in running_services:
            ecs_client.update_service(
                cluster=cluster_arn,
                service=running_service_arn.split('/')[-1],
                desiredCount=0
            )

    json_output = json.dumps(clusters_services, indent=4)
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=json_output)
    
    return {
        'statusCode': 200,
        'body': json.dumps('JSON list uploaded to S3 bucket successfully. Desired counts updated for running services.')
    }
