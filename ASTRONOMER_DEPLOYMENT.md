# 🚀 Deployment Guide - Astronomer

This guide explains how to deploy the APOD ETL pipeline to Astronomer (Airflow as a Service).

## Prerequisites

- Astronomer account (free tier available at https://www.astronomer.io/)
- Astronomer CLI installed: `curl -sSL https://install.astronomer.io | bash`
- Docker installed
- Git repository with code pushed to GitHub

## Step 1: Install Astronomer CLI

```bash
# Windows PowerShell
choco install astronomer-cli

# Or using curl (recommended)
curl -sSL https://install.astronomer.io | bash

# Verify installation
astro version
```

## Step 2: Login to Astronomer

```bash
# Login with your Astronomer credentials
astro login

# You'll be prompted to enter:
# - Email
# - Password
# - Accept terms
```

## Step 3: Create Astronomer Deployment

```bash
# Initialize Astronomer project in current directory
astro dev init

# Or create new project
astro deployment create --stack-version 6.0.0 --name apod-etl

# List your deployments
astro deployment list
```

## Step 4: Update Dockerfile for Astronomer

The `Dockerfile` included is already compatible with Astronomer. It includes:

```dockerfile
FROM apache/airflow:2.9.1-python3.10
# ... rest of setup
```

**Key additions for Astronomer**:
```dockerfile
# Already included:
- git
- ssh
- DVC
- All required Python packages
```

## Step 5: Configure Airflow Variables & Connections

### Set Environment Variables

```bash
# Create airflow_settings.yaml
astro config set AIRFLOW__CORE__EXECUTOR SequentialExecutor

# Or set via web UI (after deployment)
```

### Add PostgreSQL Connection

```bash
# In Airflow UI after deployment:
1. Admin → Connections → Create
2. Connection ID: postgres_default
3. Connection Type: Postgres
4. Host: [your-postgres-host]
5. Schema: airflow
6. Login: airflow
7. Password: [your-password]
8. Port: 5432
```

### Add NASA API Key

```bash
# In Airflow UI:
1. Admin → Variables → Create
2. Key: NASA_API_KEY
3. Value: [your-api-key or DEMO_KEY]
```

Or set as environment variable:

```bash
astro env set NASA_API_KEY "DEMO_KEY"
```

## Step 6: Build and Deploy

### Build Locally (Optional)

```bash
# Build Docker image locally
astro build

# Test locally
astro dev start

# Wait for services to start (~2 minutes)
# Access at http://localhost:8080
```

### Deploy to Astronomer Cloud

```bash
# Deploy to your deployment
astro deploy

# Select deployment when prompted

# Monitor deployment
astro deployment logs --follow
```

## Step 7: Verify Deployment

### Check Deployment Status

```bash
# Get deployment info
astro deployment info

# List deployments
astro deployment list
```

### Access Airflow UI

1. Go to https://app.astronomer.io/
2. Select your deployment
3. Click "Open Airflow"
4. Login with your Airflow credentials

### Trigger DAG

1. Navigate to DAGs in Airflow UI
2. Find `apod_etl_pipeline`
3. Click the play button to trigger

## Step 8: Configure External PostgreSQL (Optional)

If using managed PostgreSQL (e.g., AWS RDS, Azure Database):

### In Airflow UI:

```
Admin → Connections → Create New
Connection ID: postgres_default
Connection Type: Postgres
Host: your-postgres-endpoint.rds.amazonaws.com
Schema: airflow
Login: airflow
Password: [strong-password]
Port: 5432
Extra: {"sslmode": "require"}
```

### Or via astro CLI:

```bash
astro connection add postgres_default \
  --conn-type postgres \
  --conn-host your-postgres-endpoint.rds.amazonaws.com \
  --conn-schema airflow \
  --conn-login airflow \
  --conn-password [password] \
  --conn-port 5432
```

## Step 9: Set Up DVC with Cloud Storage (Optional)

For persistent DVC tracking with Astronomer:

### Option 1: DVC with S3 (AWS)

```bash
# In your repository, configure DVC remote
dvc remote add -d myremote s3://my-bucket/dvc-storage

# Create .dvc/config
# Remote section added automatically
```

### Option 2: DVC with Google Cloud Storage

```bash
dvc remote add -d myremote gs://my-bucket/dvc-storage
```

### Update Dockerfile for DVC Remote

Add to Dockerfile:
```dockerfile
# Install DVC with cloud storage support
RUN pip install dvc[s3] dvc[gs] dvc[azure]
```

## Step 10: Monitor Production Deployment

### View Logs

```bash
# Stream logs from Astronomer
astro deployment logs --follow

# Or view in Airflow UI:
# Click on tasks in DAG view
# Logs tab shows real-time execution
```

### Monitor Resources

```bash
# Check deployment metrics
astro deployment describe

# View resource usage in Astronomer UI
# https://app.astronomer.io/ → Deployment → Monitoring
```

## Scaling & Performance

### Scale Worker Resources

```bash
# Increase executor resources
astro deployment update --executor-au 10

# Or via web UI:
# Deployment Settings → Executor Resources → Adjust AU count
```

### Configure Task Resources

In your DAG:
```python
from airflow.models import Variable
from airflow.operators.python import PythonOperator

task = PythonOperator(
    task_id='extract_apod_data',
    python_callable=extract_apod,
    resources={
        "cpu_request": 200,  # millicores
        "cpu_limit": 500,
        "memory_request": 256,  # MB
        "memory_limit": 512,
    }
)
```

## Troubleshooting

### DAG not appearing

```bash
# Force DAG refresh
astro deployment logs --follow | grep -i "loading dag"

# Or trigger in UI:
# Admin → Configurations → Restart Services
```

### Connection failures

```bash
# Test connection in Airflow
# Admin → Connections → Click connection → Test

# Or via CLI
astro connection test postgres_default
```

### Memory issues

```bash
# Increase worker size
astro deployment update --executor-au 5

# Check logs for OOM
astro deployment logs | grep -i "memory\|oom"
```

## Continuous Deployment (Optional)

### GitHub Actions Integration

Create `.github/workflows/astronomer-deploy.yml`:

```yaml
name: Astronomer Deployment

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Astronomer
        env:
          ASTRONOMER_KEY_ID: ${{ secrets.ASTRONOMER_KEY_ID }}
          ASTRONOMER_KEY_SECRET: ${{ secrets.ASTRONOMER_KEY_SECRET }}
          DEPLOYMENT_ID: ${{ secrets.DEPLOYMENT_ID }}
        run: |
          curl -sSL https://install.astronomer.io | bash
          astro login --key-id $ASTRONOMER_KEY_ID --key-secret $ASTRONOMER_KEY_SECRET
          astro deploy $DEPLOYMENT_ID
```

## Cost Optimization

### Free Tier Limits

- 1 Deployment
- 5 AU (Astronomer Units)
- Limited to one DAG
- 8 GB Memory total

### Production Recommendations

- Start with 5-10 AU for small pipelines
- Use Task Pools for concurrency control
- Schedule DAGs during off-peak hours
- Enable auto-scaling if available

## Backup & Disaster Recovery

### Export Configuration

```bash
# Export DAGs
astro dags list

# Export connections
astro connection list

# Export variables
astro variable list
```

### Backup to Git

```bash
# Ensure all code is committed
git add .
git commit -m "Astronomer deployment backup"
git push origin main
```

## Next Steps

1. ✅ Verify DAG runs successfully
2. ✅ Check PostgreSQL data
3. ✅ Monitor DVC metadata commits
4. ✅ Set up monitoring alerts
5. ✅ Document deployment process

## Support

- Astronomer Docs: https://docs.astronomer.io/
- Airflow Docs: https://airflow.apache.org/docs/
- Community Slack: https://astronomer-community.slack.com/

---

**Deployment Complete! 🎉**
