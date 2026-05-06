
### to launch FastApi 
``` bash
uvicorn app.main:app --reload
```



### to merge the work to test : 
``` bash 
git checkout test
```

Then get the latest version of test:
``` bash 
git pull origin test
```

Merge your branch into test branch:
``` bash 
git merge message
```

Then push test:
``` bash 
git push origin test
```

