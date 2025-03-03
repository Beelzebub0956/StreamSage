import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = "arindam-video-storage"

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Debugging log

    # Handle CORS Preflight (OPTIONS request)
    if event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": ""
        }

    try:
        if "body" not in event or not event["body"]:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing request body"})
            }

        body = json.loads(event["body"])
        file_name = body.get("fileName")

        if not file_name:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing 'fileName' in request body"})
            }

        # Generate a Pre-Signed Upload URL
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name, 'ContentType': 'video/mp4'},
            ExpiresIn=3600
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"uploadUrl": upload_url})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"error": str(e)})
        }
