# Google Gmail API Setup Guide

To enable the "Smart" email scanning feature, you need to configure Google OAuth.

## Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., "Finance Tracker").

## Step 2: Enable Gmail API
1. In the sidebar, go to **APIs & Services** > **Library**.
2. Search for "Gmail API".
3. Click **Enable**.

## Step 3: Configure OAuth Consent Screen
1. Go to **APIs & Services** > **OAuth consent screen**.
2. Select **External** (or Internal if you have a Workspace).
3. Fill in the App Name and User Support Email.
4. Add `userinfo.email` and `userinfo.profile` scopes (and `https://www.googleapis.com/auth/gmail.readonly` if manually adding, though the app requests it).
5. Add your email as a **Test User**.

## Step 4: Create Credentials
1. Go to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth client ID**.
3. Application type: **Desktop app**.
4. Name it "Desktop Client".
5. Click **Create**.

## Step 5: Configure the App
Option A: **Download JSON**
- Download the JSON file, rename it to `client_secret.json`, and place it in the `d:/FinanceTracker` root folder.

Option B: **Environment Variables**
- Copy the `Client ID` and `Client Secret`.
- Add them to your `.env` file:
  ```env
  GOOGLE_CLIENT_ID=your_client_id
  GOOGLE_CLIENT_SECRET=your_client_secret
  ```

## Step 6: First Run
- When you click "Scan Emails" in the dashboard for the first time (or trigger the API), a browser window will open asking you to login to Google and authorize the app.
- Once authorized, a `token.json` file will be created locally, and future scans will happen automatically.
