import json
import uuid
import boto3
import os

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    method = event.get("httpMethod")

    if method == "POST":
        body = json.loads(event["body"])
        item_id = str(uuid.uuid4())

        item = {
            "id": item_id,
            "task": body.get("task"),
            "status": "pending"
        }

        table.put_item(Item=item)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Todo created", "item": item})
        }

    elif method == "GET":
        todo_id = event["pathParameters"]["id"]
        result = table.get_item(Key={"id": todo_id})
        return {
            "statusCode": 200,
            "body": json.dumps(result.get("Item", {}))
        }

    return {"statusCode": 400, "body": "Invalid request"}
