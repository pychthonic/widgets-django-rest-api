# widgets-django-rest-api


This is a REST API I built to manage widgets. It will accept GET, POST,
PUT, and DELETE requests. 

To run it, use the following commands:

```
git clone https://github.com/pychthonic/widgets-django-rest-api.git

cd widgets-django-rest-api

docker-compose build

docker-compose up

```

After that, you can first visit the swagger page at localhost:8000/swagger

The current version is 'v1' and the endpoints are:

/{version}/widgets

/{version}/widget/{id}

