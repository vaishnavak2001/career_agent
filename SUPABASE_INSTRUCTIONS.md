# ⚡ Supabase Setup Guide

## 1. Database Schema Setup
You need to create the tables in your Supabase database.

1.  **Log in** to your [Supabase Dashboard](https://supabase.com/dashboard).
2.  Select your project (`career-agent`).
3.  Go to the **SQL Editor** (icon on the left sidebar).
4.  Click **New Query**.
5.  **Copy & Paste** the entire content of the `schema.sql` file from your project.
    *   *Note: You can find `schema.sql` in the root of your GitHub repository.*
6.  Click **Run**.
    *   You should see "Success" in the results.

## 2. Connection Pooling (Crucial for Render)
Since we are using a serverless deployment on Render, we must use the Transaction Pooler to avoid running out of connections.

1.  Go to **Project Settings** -> **Database**.
2.  Scroll down to **Connection Pooling**.
3.  Ensure it is **Enabled**.
4.  Copy the **Transaction Pooler Connection String**:
    *   Mode: `Transaction`
    *   Port: `6543`
    *   It looks like: `postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`
5.  **Use this URL** as the `DATABASE_URL` in your Render Environment Variables.

## 3. Network Restrictions
1.  Go to **Project Settings** -> **Database** -> **Network Restrictions**.
2.  Ensure **"Allow access from anywhere"** (0.0.0.0/0) is enabled.
    *   *Why?* Render's IP addresses change, so we cannot whitelist specific IPs easily.
