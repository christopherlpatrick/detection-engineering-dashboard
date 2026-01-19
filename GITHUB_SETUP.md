# GitHub Setup Instructions

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `detection-engineering-dashboard` (or your preferred name)
3. Description: "Detection Engineering Simulation Dashboard - SOC portfolio project with FastAPI and React"
4. Choose: **Public** (for portfolio) or **Private** (if you prefer)
5. Do NOT initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd C:\Users\chkoo\OneDrive\Desktop\detection-engineering-dashboard

# Add your GitHub repository as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/detection-engineering-dashboard.git

# Push to GitHub
git push -u origin main
```

## Step 3: If You Need to Authenticate

If prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your password)

To create a Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Give it a name like "detection-engineering-dashboard"
4. Select scopes: `repo` (full control of private repositories)
5. Generate token and copy it
6. Use this token as your password when pushing

## Alternative: Using SSH

If you prefer SSH:

```bash
# Add SSH remote instead
git remote add origin git@github.com:YOUR_USERNAME/detection-engineering-dashboard.git

# Push
git push -u origin main
```

## Verify Upload

After pushing, visit:
`https://github.com/YOUR_USERNAME/detection-engineering-dashboard`

You should see all your files there!

## Optional: Add Topics/Tags to Your Repository

On GitHub, click on your repository settings or the gear icon to add topics like:
- `python`
- `react`
- `fastapi`
- `cybersecurity`
- `detection-engineering`
- `soc`
- `mitre-attack`
- `portfolio-project`

This helps people find your project.
