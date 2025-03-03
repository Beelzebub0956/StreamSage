import json
import boto3

SES_CLIENT = boto3.client("ses", region_name="ap-south-1")

SENDER_EMAIL = "arindam.j2004@gmail.com"
RECEIVER_EMAIL = "arindam.j2004@gmail.com"

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        video_name = body.get("videoName", "Unknown")

        response = SES_CLIENT.send_email(
            Source=SENDER_EMAIL,
            Destination={"ToAddresses": [RECEIVER_EMAIL]},
            Message={
                "Subject": {"Data": "Video Request"},
                "Body": {"Text": {"Data": f"User requested video: {video_name}"}}
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Request sent successfully!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
