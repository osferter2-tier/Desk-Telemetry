import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("current_status")

def lambda_handler(event, context):

    print(event)

    desk_code = event["pathParameters"]["desk_code"]

    response = table.get_item(
        Key={
            "desk_code": desk_code
        }
    )

    if "Item" not in response:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps({
                "error": "Desk not found"
            })
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(response["Item"])
    }
