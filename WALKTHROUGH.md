# 📖 Step-by-Step AWS Console Walkthrough: Serverless Event Announcement System

This guide documents the complete manual build of the **Serverless Event Announcement System on AWS** using **Amazon S3**, **Amazon SNS**, **AWS Lambda (Python 3.13)**, **AWS IAM**, and **Amazon API Gateway** in `us-east-1` (N. Virginia).

---

## 🏗️ Application Architecture & Roadmap

- **Frontend (`Amazon S3`):** Hosts the static website (`index.html`, `styles.css`, JS, images) and `events.json` acting as a lightweight JSON database.
- **Subscribe Flow (`POST /subscribe`):** Sends visitor emails through API Gateway to `DiorSubscribeFunction`, which registers the email with an **Amazon SNS** topic.
- **Create Event Flow (`POST /create-event`):** Sends new event submissions through API Gateway to `DiorCreateEventFunction`, which updates `events.json` in **Amazon S3** and broadcasts an email notification to all confirmed **Amazon SNS** subscribers.

---

## Step 1: Prepare Local Static Website Files

Prepare the static one-page website (`index.html`, `events.json`, `css/`, `js/`, `images/`) including the **Receive Private Invitations** subscription form, **Announce New Event** publishing form, and **Upcoming Events** feed:

![Website Hero Section](images/website-look1.png)

![Website Editorial Section](images/website-look2.png)

![Website Product Ritual Section](images/website-look3.png)

![Website Video Section](images/website-look4.png)

![Website Events & Subscription Section](images/website-look5.png)

---

## Step 2: Create & Configure the Amazon S3 Bucket

Stay in one consistent AWS Region (`us-east-1` / N. Virginia) across all services so S3, SNS, Lambda, and API Gateway communicate seamlessly.

### Step 2A: Create the S3 Bucket

1. Open **S3** in the AWS Management Console and click **Create bucket**.
2. Enter a globally unique bucket name (e.g., `dior-event-announcements-20261123`), uncheck **Block all public access**, acknowledge the public access warning, and click **Create bucket**:

![Create S3 Bucket](images/creatingBucket.png)

![S3 Bucket Created](images/createdBucket.png)

### Step 2B: Enable Static Website Hosting

1. Open the bucket's **Properties** tab -> scroll to **Static website hosting** -> click **Edit**.
2. Select **Enable**, set **Index document** to `index.html`, and click **Save changes**:

![Enable Static Website Hosting](images/enableHosting.png)

![Static Website Hosting Enabled](images/hostingEnabled.png)

3. Scroll back down to **Static website hosting** and copy your **Bucket website endpoint** URL:

![Bucket Properties](images/bucketProperties.png)

![Bucket Website Endpoint URL](images/websiteUrl.png)

### Step 2C: Attach a Public Read Bucket Policy

1. Open the **Permissions** tab -> scroll to **Bucket policy** -> click **Edit**:

![Bucket Permissions Overview](images/bucketProperties2.png)

2. Paste the public read `s3:GetObject` JSON policy (`Resource: "arn:aws:s3:::YOUR-BUCKET-NAME/*"`) and click **Save changes**:

![Edit Bucket Policy](images/bucketPolicy.png)

![Bucket Policy Saved](images/bucketPolicy3.png)

### Step 2D: Upload Website Files to S3

1. Open the **Objects** tab -> click **Upload**, drag-and-drop all contents (`index.html`, `events.json`, `css/`, `images/`, `js/`) to the root of the bucket, and click **Upload**:

![Website Files Uploaded to S3](images/UploadedWebsite.png)

2. Open your **Bucket website endpoint** URL in a browser to verify the site loads live from S3:

![Live Website Served from S3](images/SiteWorking.png)

---

## Step 3: Create the Amazon SNS Topic

### Step 3A & 3B: Create Standard Topic & Save ARN

1. Search for **SNS** in the AWS Console and open **Simple Notification Service**:

![Open SNS Service](images/sns.png)

2. Click **Topics** -> **Create topic**:

![SNS Topics Dashboard](images/createTopic.png)

3. Select **Standard** type (required for email subscriptions), enter **Name:** `dior-event-announcements` and **Display name:** `Dior Events`, and click **Create topic**:

![Configure SNS Standard Topic](images/createTopic2.png)

4. Copy and save the **Topic ARN** for Lambda environment variables in the next step:

![SNS Topic Created with ARN](images/createTopicResult.png)

---

## Step 4: Create IAM Role & Python 3.13 Lambda Functions

### Step 4A: Create Execution Role (`DiorEventLambdaRole`)

1. Open **IAM -> Roles -> Create role**:

![IAM Roles Dashboard](images/IAMCreaterole.png)

2. Select **Trusted entity type:** `AWS service` and **Use case:** `Lambda`, then click **Next**:

![Select Lambda Trusted Entity](images/creatingRole.png)

3. Attach **`AWSLambdaBasicExecutionRole`**, **`AmazonSNSFullAccess`**, and **`AmazonS3FullAccess`**, name the role **`DiorEventLambdaRole`**, and click **Create role**:

![Review IAM Role Policies](images/creatingRole2.png)

![IAM Role Created](images/roleCreated.png)

---

### Step 4B: Create Lambda #1 — `DiorSubscribeFunction` (`/subscribe`)

1. Open **AWS Lambda** (`us-east-1`) -> **Create function** (`Author from scratch`):
   - **Function name:** `DiorSubscribeFunction`
   - **Runtime:** `Python 3.13`
   - **Execution role:** Use an existing role -> **`DiorEventLambdaRole`**
2. Paste `subscribe.py` into `lambda_function.py` and click **Deploy**:

![Subscribe Lambda Code](images/pythonCodeLambdaFuntion1.png)

![Subscribe Lambda Deployed](images/function1.png)

3. Go to **Configuration -> Environment variables** -> **Edit**, add **`SNS_TOPIC_ARN`** with your SNS Topic ARN, and click **Save**:

![Subscribe Lambda Environment Variable](images/environmentVariables.png)

---

### Step 4C: Create Lambda #2 — `DiorCreateEventFunction` (`/create-event`)

1. Create a second function named **`DiorCreateEventFunction`** (`Python 3.13`, execution role **`DiorEventLambdaRole`**):

![Create Event Lambda Configuration](images/function2.png)

2. Paste `create_event.py` into `lambda_function.py` and click **Deploy**:

![Create Event Lambda Deployed](images/function2.png2.png.png)

3. Go to **Configuration -> Environment variables** -> **Edit**, add **`BUCKET_NAME`** and **`SNS_TOPIC_ARN`**, and click **Save**:

![Edit Create Event Environment Variables](images/editVariables.png)

![Create Event Environment Variables Saved](images/function2EnvironmentVariables.png)

---

## Step 5: Create API Gateway (HTTP API) & Connect Frontend

### Step 5A: Create HTTP API & Routes

1. Open **API Gateway** (`us-east-1`) and click **Create an API** -> **HTTP API**:

![API Gateway Console](images/apiGateways.png)

2. Name the API **`DiorEventsAPI`** and attach both Lambda integrations (`DiorSubscribeFunction` and `DiorCreateEventFunction`):

![Configure HTTP API Integrations](images/configurAPI.png)

3. Configure **`POST /subscribe`** -> `DiorSubscribeFunction` and **`POST /create-event`** -> `DiorCreateEventFunction`, leave the `$default` stage with auto-deploy enabled, and click **Create**:

![Configure API Gateway Routes](images/configurAPI2.png)

![Review and Create HTTP API](images/configurAPI3.png)

![HTTP API Routes Created](images/configurAPI3Result.png)

---

### Step 5B & 5C: Enable CORS & Update `index.html`

1. In the left menu under **Develop**, click **CORS** -> **Configure**:

![CORS Overview](images/cors.png)

2. Set **Access-Control-Allow-Origin** = `*`, **Access-Control-Allow-Headers** = `content-type`, and **Access-Control-Allow-Methods** = `POST`, `OPTIONS`, then click **Save**:

![Configure CORS Settings](images/cors2.png)

3. Copy the `$default` stage **Invoke URL**, paste it into `API_BASE_URL` inside `index.html`, and re-upload `index.html` to S3.

---

## Step 6: End-to-End Testing

### Test 1: Subscribe to Email Alerts

Open your S3 Website Endpoint URL (`Ctrl + F5`), enter your email in **Receive Private Invitations**, click **Subscribe**, and click **Confirm subscription** in the AWS Notification email:

![Subscribe Form Submission](images/test1.png)

![SNS Subscription Confirmation Email](images/confirmation.png)

### Test 2: Announce a New Event

Fill in **Announce New Event** and click **Publish Event**—the new event immediately saves to `events.json` in S3, appears at the top of **Upcoming Events**, and sends an email alert to all confirmed subscribers:

![New Event Published Live on Website](images/test2-result.png)

---

## 🧹 Resource Cleanup Checklist

After completing testing, delete all resources in order:

1. **API Gateway:** Delete `DiorEventsAPI`.
2. **AWS Lambda:** Delete `DiorSubscribeFunction` and `DiorCreateEventFunction`.
3. **Amazon SNS:** Delete confirmed subscriptions, then delete the `dior-event-announcements` topic.
4. **Amazon S3:** Empty and delete the S3 bucket.
5. **AWS IAM:** Delete `DiorEventLambdaRole`.
