# create conda env
```
conda create --name my_env python=3.9
conda activate my_env

```
# install dependancies
```
pip install fastapi uvicorn
pip install requests
pip install python-multipart
```

# run application

```
uvicorn app:app --reload

```