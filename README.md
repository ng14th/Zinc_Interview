## First install project
- ***Install uv package manage python at*** https://docs.astral.sh/uv/getting-started/installation/
  + **Using pip** : ***run*** ```pip/pip3 install uv```
  + **Using curl** : ***run*** ```curl -LsSf https://astral.sh/uv/install.sh | sh```

## Start Project
- **Init project** : ***run*** ``` uv venv ```
- **Sync package** : ***run*** ``` uv sync ```
- **Activate venv** : ***run*** ``` source .venv/bin/activate ```
- ***Add new package*** :  ***run*** ``` uv add {package} ```

## Run App
***Run ``` cd zinc_app ``` first***
- **Run app local** : ***run*** ``` make runserver ```
  
  + *Default app will be run on **<u>localhost:8000</u>***
  + *Change port by run command : ```python manange runserver {port}```*
  + *Or change port in Makefile*
  
  
- **Run gunicorn app** : ***run*** ``` make run-app ```
- 
  + *Default app will be run on **<u>localhost:5000</u>***
  + *Change host/port in ENV GUNICORN_HOST/ GUNICORN_PORT*
  
- **Run test case** : ***Must add file code pytest in folder test and run*** ``` make run-test ```

## Docker
***At Zinc folder*** ***run*** ``` chmod +x ./scripts/* ```
- **Build image** : ***run*** ``` ./scripts/build_image.sh ```
- **Run container after build image success** : ***run*** ``` ./scripts/run_container.sh ```