# SendGrid Setup Guide

This guide details how to obtain a SendGrid API key and configure it for your Career Agent.

## 1. Create a SendGrid Account
1.  Go to [SendGrid Signup Page](https://signup.sendgrid.com/).
2.  Select the **Free** plan (usually at the bottom or "Start for Free"). This gives you 100 emails/day forever, which is enough for this agent.
3.  Enter your email and create a password.

## 2. Verify Your Identity
1.  Check your email inbox for a verification email from SendGrid.
2.  Click the verification link.
3.  You may be asked to provide some details about your usage.
    *   **Role**: Developer
    *   **Sending volume**: 0-100 emails per month
    *   **How will you send**: Using Web API

## 3. Create a Sender Identity (Single Sender Verification)
Before you can send emails, you must verify the email address the emails will come *from*.
1.  Log in to the [SendGrid Dashboard](https://app.sendgrid.com/).
2.  In the left sidebar, go to **Settings** -> **Sender Authentication**.
3.  Click **Verify a Single Sender**.
4.  Fill in the form:
    *   **From Name**: Career Agent (or your name)
    *   **From Email**: Your personal email (e.g., `vaishnav@example.com`)
    *   **Reply To**: Same as From Email
    *   **Company Address**: You can put your home address or a placeholder if allowed.
5.  Click **Create**.
6.  Go to your email inbox again and click the verification link sent by SendGrid.
7.  Once verified, this email address will be your `EMAIL_FROM` setting.

## 4. Generate an API Key
1.  In the SendGrid Dashboard, go to **Settings** -> **API Keys**.
2.  Click **Create API Key** (top right).
3.  **API Key Name**: Give it a name like `CareerAgent_Prod`.
4.  **API Key Permissions**:
    *   Select **Full Access** (Easiest)
    *   OR Select **Restricted Access** -> Scroll to **Mail Send** -> Click the slider to give **Full Access** to Mail Send only.
5.  Click **Create & View**.
6.  **IMPORTANT**: Click on the API key to copy it. **This is the ONLY time you will see it.** Paste it into a secure note immediately.

## 5. Configure Your Application

### For Render (Production)
1.  Go to your Render Dashboard.
2.  Select your `career-agent-api` service.
3.  Go to **Environment**.
4.  Add two new variables:
    *   Key: `SENDGRID_API_KEY`
    *   Value: `SG.xxxxxxxx....` (The key you just copied)
    *   Key: `EMAIL_FROM`
    *   Value: `your_verified_email@example.com` (The email you verified in Step 3)
5.  Save Changes. Render will redeploy automatically.

### For Local Development
1.  Open your `.env` file.
2.  Add:
    ```env
    SENDGRID_API_KEY=SG.xxxxxxxx....
    EMAIL_FROM=your_verified_email@example.com
    ```

## 6. Testing
The agent is configured to send an email alert whenever it finds new jobs that match your criteria. You can trigger a scrape manually to test this.
