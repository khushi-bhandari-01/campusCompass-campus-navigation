# GitHub Setup Guide

## 1. Account and repository
1. Create an account at https://github.com/signup and verify your email.
2. Click **+ > New repository**. Name it `pathfinder-campus-navigation`, keep it **Public** (or Private), and **do not** tick "Add a README" or ".gitignore" (the project already has them). Click **Create repository** and keep the page open.

## 2. Configure Git (once per computer)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
Use the same email as your GitHub account.

## 3. Open the project in VS Code
**File > Open Folder > PATHFINDER**, then **Terminal > New Terminal** (it opens in the project root).

## 4. Initialise and make the first commit
```bash
git init
git branch -M main
git add .
git status
git commit -m "Initial commit: PATHFINDER A* campus navigation"
```
`git status` should NOT list `node_modules`, `.venv`, `dist` or any `.env` file (they are in `.gitignore`).

## 5. Connect and push
Copy your repository URL from GitHub (HTTPS), then:
```bash
git remote add origin https://github.com/YOUR-USERNAME/pathfinder-campus-navigation.git
git push -u origin main
```
GitHub asks you to sign in in the browser (or use a Personal Access Token as the password: GitHub > Settings > Developer settings > Tokens). Refresh the repository page to see your files.

## 6. Updating after changes
```bash
git status
git add .
git commit -m "Describe what changed"
git push
```
Pushing to `main` also triggers automatic redeploys on Vercel and Render once connected.

## 7. Branches
```bash
git switch -c feature/improve-legend     # create and switch
# ...edit, then:
git add . && git commit -m "Improve map legend contrast"
git push -u origin feature/improve-legend
```
On GitHub click **Compare & pull request**, review, then **Merge**. Back locally: `git switch main && git pull`.

## 8. Good commit messages
Short, present tense, say what and why: `Fix swap button when only source is set`, `Add Dijkstra benchmark`, `Document Render deployment`. Avoid `update` or `final2`.

## 9. Secrets
Never commit passwords, tokens or `.env` files. Only `.env.example` files (placeholders) belong in the repo. This project needs no API keys. If you commit a secret by accident, revoke it immediately; deleting the file later does not remove it from history.
