### to launch FastApi

```bash
uvicorn app.main:app --reload
```

### to merge the work to test :

```bash
git checkout test
```

Then get the latest version of test:

```bash
git pull origin test
```

Merge your branch into test branch:

```bash
git merge message
```

Then push test:

```bash
git push origin test
```

# remove your accidental changes from local TEST BRANCH

```bash
git reset --hard origin/test
```
This will make the local test branch exactly the same as GitHub test branch

# create hugging face token

we go on the link of our profile , we create new token after this we go to terminal we authentificate and paste our token 
```bash
hf auth login
```

