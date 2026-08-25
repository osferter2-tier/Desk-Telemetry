import json
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource("dynamodb")

desks_table = dynamodb.Table("desks")
assignments_table = dynamodb.Table("expected_assignments")
events_table = dynamodb.Table("telemetry_events")
status_table = dynamodb.Table("current_status")

REQUIRED_FIELDS = [
    "hostname",
    "monitor_id",
    "timestamp",
    "agent_version"
]

def lambda_handler(event, context):

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    missing_fields = []

    for field in REQUIRED_FIELDS:
        if field not in body:
            missing_fields.append(field)

    if missing_fields:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "received": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            })
        }

    hostname = body["hostname"]
    monitor_id = body["monitor_id"]
    timestamp = body["timestamp"]
    agent_version = body["agent_version"]

    # ==================================================
    # NO_MONITOR Handling
    # ==================================================

    if monitor_id == "NO_MONITOR":

        event_id = str(uuid.uuid4())

        events_table.put_item(
            Item={
                "event_id": event_id,
                "hostname": hostname,
                "monitor_id": monitor_id,
                "desk_code": "DESK-20",
                "timestamp": timestamp,
                "agent_version": agent_version,
                "calculated_status": "NO_MONITOR"
            }
        )

        status_table.put_item(
            Item={
                "desk_code": "DESK-20",
                "current_hostname": hostname,
                "expected_hostname": "",
                "monitor_id": "",
                "status": "NO_MONITOR",
                "last_report": timestamp
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "received": True,
                "desk_code": "DESK-20",
                "status": "NO_MONITOR"
            })
        }

    # ==================================================
    # Find desk by monitor
    # ==================================================

    desk_code = None

    desks = desks_table.scan()

    for item in desks["Items"]:
        if item["monitor_id"] == monitor_id:
            desk_code = item["desk_code"]
            break

    if not desk_code:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "received": True,
                "status": "UNKNOWN_MONITOR"
            })
        }

    # ==================================================
    # Determine assignment status
    # ==================================================

    today = datetime.utcnow().strftime("%Y-%m-%d")

    assignment = assignments_table.get_item(
        Key={
            "assignment_date": today,
            "desk_code": desk_code
        }
    )

    if "Item" not in assignment:

        calculated_status = "NO_ASSIGNMENT"
        expected_hostname = None

    else:

        expected_hostname = assignment["Item"]["expected_hostname"]

        if hostname.upper() == expected_hostname.upper():
            calculated_status = "OK"
        else:
            calculated_status = "UNASSIGNED_DEVICE"

    # ==================================================
    # Mark previous desks as VACANT
    # ==================================================

    current_status = status_table.scan()

    for existing in current_status["Items"]:

        existing_hostname = existing.get(
            "current_hostname",
            ""
        )

        existing_desk = existing.get(
            "desk_code",
            ""
        )

        if (
            existing_hostname.upper() == hostname.upper()
            and existing_desk != desk_code
        ):

            status_table.put_item(
                Item={
                    "desk_code": existing_desk,
                    "current_hostname": "",
                    "expected_hostname": existing.get(
                        "expected_hostname",
                        ""
                    ),
                    "monitor_id": existing.get(
                        "monitor_id",
                        ""
                    ),
                    "status": "VACANT",
                    "last_report": timestamp
                }
            )

    # ==================================================
    # Store telemetry event
    # ==================================================

    event_id = str(uuid.uuid4())

    events_table.put_item(
        Item={
            "event_id": event_id,
            "hostname": hostname,
            "monitor_id": monitor_id,
            "desk_code": desk_code,
            "timestamp": timestamp,
            "agent_version": agent_version,
            "calculated_status": calculated_status
        }
    )

    # ==================================================
    # Update current status
    # ==================================================

    status_table.put_item(
        Item={
            "desk_code": desk_code,
            "current_hostname": hostname,
            "expected_hostname": expected_hostname or "",
            "monitor_id": monitor_id,
            "status": calculated_status,
            "last_report": timestamp
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "received": True,
            "desk_code": desk_code,
            "status": calculated_status
        })
    }
