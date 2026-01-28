# Table Setup

## BigQuery Setup

### Step 1: Create a Google Cloud Project

1. Create a new Google project by following the first three steps [here](https://docs.cloud.google.com/bigquery/docs/pre-built-tools-with-mcp-toolbox#begin).

   **Note:** In step 2, you will be asked to enable billing in your Google Cloud Project. Since the table you will work with is very small and BigQuery has a free tier, executing the small queries shown in the video won't cost anything. Make sure to delete the table you create when you're done.

2. Suggested name for the Google Cloud Project: `claude-skills-lab` or `skills-training-lab`
3. Note your `Project ID`

### Step 2: Create a Dataset

1. Go to [console.cloud.google.com/bigquery](https://console.cloud.google.com/bigquery)
2. Click the **three dots** next to your project ID
3. Click **"Create dataset"**
4. Dataset ID: `marketing`
5. Choose your region (e.g., `us-west1`)
6. Click **Create Dataset**

### Step 3: Upload CSV Data

1. Click the **three dots** next to your `marketing` dataset
2. Click **"Create table"**
3. Source: **Upload** → select your CSV file (campaign_performance_4weeks.csv)
4. Table name: `campaign_performance`
5. Schema: Check **"Auto detect"**
6. Click **Create table**

## BigQuery MCP Server Setup

To create the credentials needed to connect to BigQuery, there is more than one option. You can review them [here](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment). For this course, we went with the option of creating a service account.

### Step 1: Create a Service Account

1. Go to [console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Select your project (e.g., `claude-skills-lab`)
3. Click **"Create Service Account"**
4. Name: `claude-bigquery-reader`
5. Click **Create and Continue**
6. Grant roles:
   - `roles/bigquery.dataViewer`
   - `roles/bigquery.user`
7. Click **Continue** and then **Done**

### Step 2: Create JSON Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Choose **JSON**
5. Download the file (keep it safe!)

### Step 3: Add MCP to Claude Desktop Config

1. [Install the MCP toolbox](https://github.com/googleapis/genai-toolbox?tab=readme-ov-file#installing-the-server) (you only need to install the toolbox server; you don't need to run it)

2. In Claude Desktop, go to: `Settings` → `Developer` → `Edit Config` and add:
```json
    {
        "mcpServers": {
            "bigquery": {
                "command": "./PATH/TO/toolbox",
                "args": ["--prebuilt","bigquery","--stdio"],
                "env": {
                    "BIGQUERY_PROJECT": "your_BigQuery_Project_ID",
                    "GOOGLE_APPLICATION_CREDENTIALS":"path/to/JSON_Key"
                }
            }
        }
    }
```

3. Restart Claude Desktop to load the new settings.

## References

- [Connect LLMs to BigQuery with MCP](https://docs.cloud.google.com/bigquery/docs/pre-built-tools-with-mcp-toolbox)

## SQLite Setup

There is more than one way to create a SQLite database. Here's the Pythonic way.

### Step 1: Install pandas (if needed)
```bash
pip install pandas
```

### Step 2: Write the Python script
```python
import pandas as pd
import sqlite3

# Read the CSV file
df = pd.read_csv('yourfile.csv')

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Import CSV data into a table
df.to_sql('tablename', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
```

### Step 3: Run the script
```bash
python your_script.py
```

This will create the database `mydatabase.db` in your current working directory.

### Step 4: Verify the import
```python
import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Check the data
cursor.execute('SELECT * FROM tablename LIMIT 5')
print(cursor.fetchall())

conn.close()
```