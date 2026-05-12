### to launch FastApi

```bash
uvicorn app.main:app --reload
```
### docker 
```bash

```

# Make sure you are on your branch
git checkout message

# Download all branches from GitHub
git fetch origin

# Merge the frontend branch into your current branch (message)
git merge origin/frontend

# Push the updated message branch to GitHub
git push origin message

# remove your accidental changes from local TEST BRANCH

```bash
git reset --hard origin/test
```
This will make the local test branch exactly the same as GitHub test branch
