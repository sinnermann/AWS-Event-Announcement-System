import json
import os
import boto3

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET_NAME = os.environ["BUCKET_NAME"]
TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
FILE_KEY = "events.json"

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        title = body.get("title", "").strip()
        date = body.get("date", "").strip()
        description = body.get("description", "").strip()

        if not title or not date or not description:
            return response(400, {"message": "Title, date, and description are required."})

        try:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
            events = json.loads(obj["Body"].read().decode("utf-8"))
        except s3.exceptions.NoSuchKey:
            events = []

        events.insert(0, {
            "title": title,
            "date": date,
            "description": description
        })

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_KEY,
            Body=json.dumps(events, indent=2),
            ContentType="application/json"
        )

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"New Dior Event: {title}",
            Message=(
                f"A new event has been announced at House of Dior:\n\n"
                f"Event: {title}\n"
                f"Date: {date}\n"
                f"Details: {description}\n\n"
                f"Visit our website to view all upcoming events."
            )
        )

        return response(200, {"message": "Event published and subscribers notified!"})
    except Exception as e:
        return response(500, {"message": f"Error: {str(e)}"})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
