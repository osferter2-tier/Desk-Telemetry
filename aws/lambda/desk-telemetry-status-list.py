import json
import boto3

dynamodb = boto3.resource("dynamodb")

status_table = dynamodb.Table("current_status")
employee_table = dynamodb.Table("employee_directory")

def lambda_handler(event, context):

    response = status_table.scan()

    results = []

    for item in response["Items"]:

        hostname = item.get("current_hostname", "")

        employee_name = "Unknown"

        if hostname:

            employee = employee_table.get_item(
                Key={
                    "hostname": hostname
                }
            )

            if "Item" in employee:
                employee_name = employee["Item"].get(
                    "employee_name",
                    "Unknown"
                )

        item["employee_name"] = employee_name

        results.append(item)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(results)
    }
