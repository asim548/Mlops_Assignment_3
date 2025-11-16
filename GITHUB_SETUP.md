# 🔗 GitHub Setup & Submission Guide

## Your GitHub Repository

**Repository URL:**
```
https://github.com/asim548/Mlops_Assignment_3.git
```

**Repository Details:**
- Owner: asim548
- Repository Name: Mlops_Assignment_3
- Branch: main

**✅ Setup is complete!** Your repository is ready to use.

---

## Step 1: Connect Local Repository to GitHub

### Option A: Using GitHub Web UI

1. Go to https://github.com/new
2. Repository name: `Mlops_Assignment_3` or `Mlops_22i_2679_A3`
3. Description: "MLOps Assignment 3: NASA APOD Data Pipeline"
4. Choose: **Public** (for assignment submission)
5. Initialize with: ✓ Add .gitignore (Python)
6. Click "Create repository"

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI if needed
# https://cli.github.com/

gh repo create Mlops_Assignment_3 \
  --description "MLOps Assignment 3: NASA APOD Data Pipeline" \
  --public
```

---

## Step 2: Connect Local Repository to GitHub

### Configure Git Credentials

```powershell
# Windows PowerShell

# Set global Git user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Or local repo only
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"

# Verify
git config --list
```

### Option A: HTTPS (Simpler)

```bash
# In your local repository directory
cd c:\Users\Aaim Shehzad\OneDrive\Desktop\7\MLOPs\Mlops_22i_2679_A3

# Remove existing remote (if any)
git remote remove origin

# Add GitHub remote
git remote add origin https://github.com/asim548/Mlops_Assignment_3.git

# Push code
git branch -M main
git push -u origin main

# When prompted, use Personal Access Token (PAT) for password
```

**Generate GitHub Personal Access Token:**
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → Select `repo` scope
3. Copy token and use as password in Git

### Option B: SSH (More Secure)

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub  # Linux/Mac
# or
type %USERPROFILE%\.ssh\id_ed25519.pub  # Windows PowerShell
```

**Add SSH key to GitHub:**
1. GitHub Settings → SSH and GPG keys → New SSH key
2. Paste your public key
3. Save

```bash
# Configure Git to use SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Test connection
ssh -T git@github.com

# Add remote
git remote add origin git@github.com:asim548/Mlops_Assignment_3.git

# Push code
git push -u origin main
```

---

## Step 3: Initial Push to GitHub

```bash
# Verify you're in the correct directory
pwd  # Should show: .../Mlops_Assignment_3

# Check Git status
git status

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete MLOps APOD ETL Pipeline

- Implemented all 5 pipeline steps (Extract, Transform, Load, DVC, Git)
- Airflow DAG with sequential task execution
- PostgreSQL integration for data storage
- DVC for data versioning
- Git integration for metadata commits
- Comprehensive documentation and tests"

# Push to GitHub
git push -u origin main

# Verify
git log --oneline -5
git remote -v
```

---

## Step 4: Enable Git Integration in Pipeline

Once your repository is set up, the pipeline can automatically commit changes.

### Update Environment Variables

```bash
# Add to .env file
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com

# Or set as environment variable
$env:GIT_USER_NAME = "Your Name"
$env:GIT_USER_EMAIL = "your.email@example.com"
```

### Verify Git Access from Docker

```bash
# Test Git access in Docker container
docker-compose exec airflow git config --list

# Test remote access
docker-compose exec airflow git ls-remote origin HEAD
```

---

## Step 5: Monitor GitHub Updates

After the pipeline runs successfully, you should see:

1. **New DVC Metadata Files** in Git commits:
   ```
   data/processed/apod_data.csv.dvc
   ```

2. **Commit History** showing automatic commits from Airflow:
   ```
   Update DVC metadata: data/processed/apod_data.csv.dvc
   Author: Airflow Pipeline <airflow@mlops.local>
   ```

3. **Repository Structure**:
   ```
   your-repo/
   ├── airflow/
   ├── postgres/
   ├── data/
   ├── tests/
   ├── README.md
   ├── docker-compose.yml
   ├── Dockerfile
   ├── dvc.yaml
   └── [DVC metadata files]
   ```

---

## Step 6: Repository Best Practices

### Initial Setup

```bash
# Create meaningful Git branches (optional)
git branch -b develop
git checkout develop
# Make changes
git push -u origin develop

# Later, merge to main for releases
git checkout main
git merge develop
git push origin main
```

### Regular Commits

```bash
# Commit structure
git add [specific-files]
git commit -m "Brief description

Detailed explanation if needed:
- What changed
- Why it changed
- Any relevant references"
```

### Repository Documentation

Ensure these files are in root:
- ✅ `README.md` - Project overview
- ✅ `SETUP.md` - Installation guide
- ✅ `ARCHITECTURE.md` - Technical design
- ✅ `requirements.txt` - Dependencies
- ✅ `LICENSE` - (Optional) Add appropriate license

---

## Step 7: Example GitHub Workflow

### Before First Run

```bash
# 1. Initialize and first commit
git init
git add .
git commit -m "Initial: Complete MLOps pipeline implementation"

# 2. Create GitHub repository
# ... via GitHub web or CLI ...

# 3. Push initial code
git remote add origin https://github.com/yourusername/Mlops_Assignment_3.git
git branch -M main
git push -u origin main
```

### After Pipeline Execution

```bash
# Pipeline runs automatically and commits DVC metadata:

# On GitHub, you'll see:
# Commit: "Update DVC metadata: data/processed/apod_data.csv.dvc"
# Changed files: data/processed/apod_data.csv.dvc
# Author: Airflow Pipeline

# You can verify by viewing:
# https://github.com/yourusername/Mlops_Assignment_3/commits/main
```

### Manual Verification

```bash
# Check what pipeline would commit
git status

# View pending changes
git diff

# If needed, manually stage specific files
git add data/processed/apod_data.csv.dvc
git commit -m "Manual DVC metadata update"
git push origin main
```

---

## Troubleshooting GitHub Integration

### Issue: "Authentication Failed"

**Solution for HTTPS:**
```bash
# Use Personal Access Token instead of password
# Generate at: https://github.com/settings/tokens

# Clear cached credentials (Windows)
git credential-manager erase https://github.com
git push  # Will prompt for new credentials
```

**Solution for SSH:**
```bash
# Test SSH connection
ssh -T git@github.com

# If it fails, check key permissions
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### Issue: "Repository Not Found"

**Solution:**
```bash
# Verify remote URL
git remote -v

# Update if needed
git remote set-url origin https://github.com/yourusername/correct-repo.git
```

### Issue: "Permission Denied"

**Solution:**
```bash
# Check if repository exists
curl https://api.github.com/repos/yourusername/Mlops_Assignment_3

# Verify access permissions
git push --set-upstream origin main --verbose
```

### Issue: "Git Push from Docker Fails"

**Solution:**
```bash
# Mount .git directory to container
# In docker-compose.yml:
volumes:
  - ./.git:/opt/airflow/.git

# Or configure SSH in container
docker-compose exec airflow git config --global user.name "Your Name"
docker-compose exec airflow ssh-add ~/.ssh/id_ed25519
```

---

## Step 8: Assignment Submission Checklist

Before submitting, verify:

- [ ] GitHub repository created
- [ ] Code pushed to `main` branch
- [ ] All commits visible in GitHub
- [ ] DVC metadata files present
- [ ] `.gitignore` configured
- [ ] `README.md` explains the project
- [ ] Tests passing locally
- [ ] Documentation complete
- [ ] Docker setup working
- [ ] Pipeline executes end-to-end

### Final Submission

1. **Share Repository URL**
   ```
   https://github.com/asim548/Mlops_Assignment_3.git
   ```

2. **Verify Access**
   - [ ] Public repository
   - [ ] Readable files
   - [ ] Full history visible

3. **Document Completion**
   ```
   GitHub Repository: https://github.com/asim548/Mlops_Assignment_3.git
   Assignment: MLOps Assignment 3
   Student: Aaim Shehzad
   Date: November 16, 2025
   Status: COMPLETE ✓
   ```

---

## Next Steps After Setup

1. ✅ Run the pipeline in Docker
2. ✅ Verify data flows through all 5 steps
3. ✅ Check GitHub for automatic commits
4. ✅ Query PostgreSQL for data
5. ✅ Review DVC metadata files
6. ✅ Document any issues
7. ✅ Submit assignment with repository URL

---

## Important Notes

### Git Credentials Security

⚠️ **NEVER commit these to Git:**
- `.env` file with API keys
- Database passwords in plain text
- SSH private keys
- Personal access tokens

✅ **Always use:**
- `.env` file (add to `.gitignore`)
- Environment variables
- Secrets manager for production
- SSH keys (private key NOT committed)

### DVC Configuration

If using DVC remote storage (AWS S3, Google Cloud, etc.):

```bash
# Configure remote
dvc remote add -d myremote s3://my-bucket/dvc-storage

# Credentials via environment
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx

# DVC remote config is tracked in Git (safe to commit)
git add .dvc/config
git commit -m "Configure DVC remote storage"
```

---

## Support Resources

- **GitHub Docs**: https://docs.github.com/
- **Git Guide**: https://git-scm.com/book/
- **GitHub CLI**: https://cli.github.com/

---

**Ready to Submit!** 🚀

Once your repository is set up, follow the SETUP.md instructions to run the pipeline and watch it automatically update your repository with DVC metadata!
