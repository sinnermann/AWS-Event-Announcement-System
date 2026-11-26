# 📢 Serverless Event Announcement System on AWS (S3 + API Gateway + Lambda + SNS)

👉 **[Click here to view the full Step-by-Step AWS Console Walkthrough & Screenshots](WALKTHROUGH.md)**

An event-driven, serverless web application built on AWS that allows visitors to subscribe to email alerts and enables administrators to publish new events—automatically updating the live S3-hosted website and broadcasting notifications to subscribers via Amazon SNS.

## How It Works

1. **Static Frontend (`Amazon S3`):** Hosts the HTML/CSS/JS website (`index.html`) and uses `events.json` as a lightweight database for upcoming events.
2. **API Layer (`Amazon API Gateway - HTTP API`):** Exposes two CORS-enabled `POST` routes (`/subscribe` and `/create-event`).
3. **Subscription Flow (`DiorSubscribeFunction` - AWS Lambda Python 3.13):** Receives visitor email addresses from `/subscribe` and registers them to an **Amazon SNS** topic (double opt-in confirmation).
4. **Event Publishing Flow (`DiorCreateEventFunction` - AWS Lambda Python 3.13):** Receives new event details from `/create-event`, prepends the event to `events.json` inside **Amazon S3**, and publishes an email notification to all confirmed **Amazon SNS** subscribers.

## AWS Services Used

- **Amazon S3:** Static website hosting and JSON persistence (`events.json`).
- **Amazon API Gateway:** HTTP API (`$default` stage) with CORS configured for browser requests.
- **AWS Lambda:** Serverless Python 3.13 (`boto3`) compute configured via environment variables (`BUCKET_NAME`, `SNS_TOPIC_ARN`).
- **Amazon SNS:** Standard Pub/Sub topic managing email subscriptions and fan-out notifications.
- **AWS IAM:** Execution role (`DiorEventLambdaRole`) granting Lambda permissions for CloudWatch Logs, S3, and SNS.

## Files in This Repository

- `subscribe.py` — Python 3.13 Lambda function handling SNS email subscriptions
- `create_event.py` — Python 3.13 Lambda function updating S3 `events.json` and publishing SNS alerts
- `WALKTHROUGH.md` — Complete step-by-step AWS Management Console build guide with screenshots
- `images/` — Console screenshots from each deployment and testing phase
