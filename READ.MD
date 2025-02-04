# Super Secure Api
## Password manager

# Arquitecture

![](https://i.ibb.co/tpR2FPhC/diagram.png)


### Tech stack 
- Python 3.12
- Django 5
- Postgres
- Docker
- Kubernetes

### Django Libraries:

- Django Rest Framework
- Django JWT
- Django Storages
- Boto3
- Pillow


### Requirements:

- Docker Desktop https://www.docker.com/products/docker-desktop/
- Terminal
- Create S3 Bucket to store the files

## Instructions

- Clone the repo
- go to the folder and copy env_template to .env:  `cp env_template .env`
- change the variables

## Create S3 bucket: and set policies and variables on .env file
https://medium.com/@hrushi669/file-storage-with-aws-s3-buckets-upload-for-the-django-project-50ea7208c4b1

## Generate sengrid api key
https://www.twilio.com/docs/sendgrid/ui/account-and-settings/api-keys

Once you have done with all the requirements you can start the backend

### run this command:

`docker-compose up`

that command will raise the database on local and the backend as well

- To access to the api docs go to: http://localhost:9090/ultra-secure

- To access to admin go to: http://localhost:9090/ultra-secure/admin

- To run migrations: `docker compose run --rm api python manage.py migrate`
- To create admin user: `docker compose run --rm api python manage.py createsuperuser`
- To stop destroy all the containers: `docker compose down`




