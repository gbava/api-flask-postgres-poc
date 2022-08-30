

# 1. Pick an API implementation

## titanic-api: Flask

Implemented using [Flask][] Python microframework.

## Installation and launching

### Clone

Clone the repo:

``` bash
git clone git@gitlab.com:ContainerSolutions/titanic-api.git
cd titanic-api/python/
```

### Install

Use [venv][] or any other ([Pipenv][], [Poetry][], etc) [environment management][] tool to install dependencies in the same folder.
Activate virtual environment and run:

``` bash
pip install -r requirements.txt
```

### Launch

This API was tested using postgres. In order to bring it up, the following commands are needed:

1) Start postgres locally with:

```
docker run --net=host --name titanic-db -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -d postgres
```
2) Copy the sql file with the database definition:

```
docker cp titanic.sql titanic-db:/
```


3) Import the sql file with: 

```
docker exec -it --rm titanic-db psql -U user -d postgres -f titanic.sql
```


After you have database server deployed and running, use environment variable `DATABASE_URL` to provide database connection string.

``` bash
DATABASE_URL=postgresql+psycopg2://user:password@127.0.0.1:5432/postgres python run.py
```

Go to <http://127.0.0.1:5000/> in your browser.

Test it by:
1) See the database is currently empty with: `http://127.0.0.1:5000/people`
2) Add a new user with `curl -H "Content-Type: application/json" -X POST localhost:5000/people -d'{"survived": 2,"passengerClass": 2,"name": "Mr. Owen Harris Braund","sex": "male","age": 22.0,"siblingsOrSpousesAboard": 4,"parentsOrChildrenAboard": 5,"fare": 7.25}`

3) Check out if the user was added with:

```
curl -X GET http://127.0.0.1:5000/people | jq
```



# 2. Setup & fill database

I've created the ```manage.py``` which has two methods:

**recreate_db()**

Will recreate the DB and the *people* table.

**seed_db()**

Will populate the DB with a modified version of [titanic.csv](https://gitlab.com/ContainerSolutions/titanic-api/-/blob/master/titanic.csv) 

(I've only added the column uuid and filled it with random generated *uuids*)

# 3. Dockerize

**Define environment variables in a file**

Using environment variables is helpful because it ensures that the code is flexible. 

Create `.env` file with the following variables:

```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=postgres
FLASK_ENV=development
PG_SERVICE_NAME=postgres-service
APP_SETTINGS=src.config.Development
```

**Build image**

*Use BuildKit feature*
```
DOCKER_BUILDKIT=1 docker build -t titanic-api-flask .
```

**Run Postgresql container**

```
docker run --net=host --name titanic-db -e POSTGRES_PASSWORD=DyUF0njM -e POSTGRES_USER=api_test_user -d postgres
```

**Run Flask API container**
```
docker run --net=host --env-file .env -t -p 50000:5000 titanic-api-flask 
```

# 4. Deploy to Kubernetes

#### Creating the volume for DB storage

```
kubectl apply -f ./k8s/pv.yml
kubectl apply -f ./k8s/pvc.yml 
```

#### Creating a configmap for consuming environment variables 

```
kubectl apply -f ./k8s/configmap.yml
```

#### Creating the database credentials
```
kubectl apply -f ./k8s/secret.yml
```

#### Creating the postgres deployment and service
```
kubectl create -f ./k8s/postgres-deployment.yml
kubectl create -f ./k8s/postgres-service.yml
```


#### Creating the Flask API deployment and service
```
kubectl create -f ./k8s/app-deployment.yml
kubectl create -f ./k8s/app-service.yml
```

#### Add LoadBalancer or Ingress
Todo

# 5. Whatever you can think of

- Implement a CI/CD pipeline
- Configure a logging or monitoring system
- Scan the Docker image for security vulnerabilities
- Create Helm charts
- Security