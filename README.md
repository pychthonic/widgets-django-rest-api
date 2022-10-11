# widgets-django-rest-api


This is a REST API I built to manage widgets. It will accept GET, POST,
PUT, and DELETE requests. 

To run it locally, use the following commands:

```
git clone https://github.com/pychthonic/widgets-django-rest-api.git

cd widgets-django-rest-api

docker-compose build

docker-compose up

```

After that, you can first visit the swagger page at localhost:8000/swagger

The current version is 'v1' and the endpoints are:

To get a list of all widgets currently in the database, send a GET
request to this endpoint,

/{version}/widgets/

like so:

```
curl --request GET 'localhost:8000/v1/widgets/' \
--header 'Content-Type: application/json'
```

To get information on a specific widget, send a GET request to
/{version}/widgets/{id}

like so:

```
curl --request GET 'localhost:8000/v1/widgets/id/1' \
--header 'Content-Type: application/json'
```

To create a new widget with name "new widget", of type "heatMap", send
a POST request to /{verions}/widgets

like so:

```
curl --request POST 'localhost:8000/v1/widgets/' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "new widget", "widget_type": "heatMap"}'
```

To change the name of widget with id 3 to "new heat map widget", send a 
PUT request to /{version}/widgets/3 with a request body of
{"name": "new heat map widget"}

like so:

```
curl --request PUT 'localhost:8000/v1/widgets/id/3' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "new heat map widget"}'
```

To delete widget with id 3, send a DELETE request to /{version}/widgets/id/3

like so:

```
curl --request DELETE 'localhost:8000/v1/widgets/id/3' \
--header 'Content-Type: application/json'
```

