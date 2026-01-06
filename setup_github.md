# Setting Up GitHub Repository

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `hosts-file-guardian` (or your preferred name)
3. Description: "Windows application that monitors and protects the hosts file from unauthorized changes"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd C:\Users\LEON\Desktop\hosts
git remote add origin https://github.com/YOUR_USERNAME/hosts-file-guardian.git
git branch -M main
git push -u origin main
```

Or if you prefer SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/hosts-file-guardian.git
git branch -M main
git push -u origin main
```

## Step 3: Verify

Visit your repository on GitHub to confirm all files are uploaded.

## Future Updates

To push future changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

