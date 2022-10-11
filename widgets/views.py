"""Django views are Pythonfunctions that take http requests and return
http responses. Since this is a REST API, the functions return http
responses with JSON objects in their response bodies.
"""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request    # used for type hints
from rest_framework.response import Response

from .env import APP_VERSION
from .models import Widget
from .models import WIDGET_TYPES
from .serializers import WidgetSerializer

@swagger_auto_schema(methods=['POST'], request_body=WidgetSerializer)
@api_view(['GET', 'POST'])
def widgets(request: Request,
            version: str,
            widget_type: str = None) -> Response:
    """
    GET request returns all widgets in the database. If a
    widget_type is provided as part of the URL parameters, then only
    widgets of that type are returned.
    POST request is used to create a new widget in the database
    with data from the POST request body.
    """

    if version != APP_VERSION:
        response_body = {
                'Error': f"Invalid API version: {version}"}
        return Response(response_body,
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if widget_type:
            widgets_list = Widget.objects.filter(widget_type=widget_type)
        else:
            widgets_list = Widget.objects.all()

        serializer = WidgetSerializer(widgets_list, many=True)

        response_body = {'widget_query_count': len(serializer.data),
                         'widgets': serializer.data}
        return Response(response_body,
                        status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = WidgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_body = {'added': serializer.data}
            return Response(response_body,
                            status=status.HTTP_201_CREATED)
        else:
            response_body = {
                'Error': f"Invalid request body: {serializer.errors}"}
            return Response(response_body,
                            status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['PUT'], request_body=WidgetSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
def widget(request: Request,
           version: str,
           id: int) -> Response:
    """
    Used to get, update and delete a specific widget.
    It takes in the request, API version and widget id as parameters.
    GET request: returns the serialized data for that particular
    widget using WidgetSerializer class.
    PUT request: Use WidgetSerializer class to validate our input data
    and save changes if valid.
    DELETE request: delete that particular widget from database.
    """

    if version != APP_VERSION:
        response_body = {
                'Error': f"Invalid API version: {version}"}
        return Response(response_body,
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        widget = Widget.objects.get(pk=id)
    except Widget.DoesNotExist:
        response_body = {"Error": "Invalid Widget ID"}
        return Response(response_body, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WidgetSerializer(widget)
        response_body = {"widget": serializer.data}
        return Response(response_body, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = WidgetSerializer(widget, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_body = {"updated_widget": serializer.data}
            return Response(response_body, status=status.HTTP_200_OK)
        else:
            response_body = {"Error": serializer.errors}
            return Response(response_body,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        widget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def widget_types(request: Request,
                 version: str) -> Response:
    """
    Used to get a list of all the widget types that are available.
    It is called by the GET method and returns a JSON response with two
    lists, one for widget types in use and another for all available
    widget types.

    A POST method could be added to this endpoint to allow
    an enduser to add to available types. A table could also be
    added to the database called types, which would keep track
    of what types are available and how many of each are in use.
    """

    if version != APP_VERSION:
        response_body = {
                'Error': f"Invalid API version: {version}"}
        return Response(response_body,
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':

        widgets_list = Widget.objects.all()
        serializer = WidgetSerializer(widgets_list, many=True)

        types_used = set()
        for widget_instance in serializer.data:
            types_used.add(widget_instance['widget_type'])

        response_body = {
            'widget_types_available': [t[0] for t in WIDGET_TYPES],
            'widget_types_in_use': list(types_used)
            }
        return Response(response_body,
                        status=status.HTTP_200_OK)
    elif request.method == 'POST':
        pass   # To be filled in. See endpoint comments.
