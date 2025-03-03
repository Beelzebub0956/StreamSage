import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Debugging line

    try:
        if 'body' not in event or not event["body"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing body in request"})
            }

        data = json.loads(event["body"])
        file_name = data.get("fileName") or data.get("filename")

        if not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'fileName' in request body"})
            }

        if not BUCKET_NAME:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Missing 'BUCKET_NAME' environment variable"})
            }

        stream_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=3600
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Successfully generated streaming URL", "streamUrl": stream_url})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format in request body"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
