"""These tests are not comprehensive yet, but they do cover the four
request types for a CRUD application: get, post, put, delete.
"""

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.views import status

from .models import Widget
from .serializers import WidgetSerializer
from .views import widget
from .views import widgets


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_widget(name="",
                      author="backend dev 3",
                      widget_type="unspecifiedType"):
        Widget.objects.create(name=name,
                              author=author,
                              widget_type=widget_type)

    def setUp(self):
        # add test data
        self.create_widget("widget 1")
        self.create_widget("Heat Map Widget", widget_type="heatMap")
        self.create_widget("Range Widget", widget_type="range")
        self.create_widget("Grid Widget 1", widget_type="grid")
        self.create_widget("Grid Widget 2", widget_type="grid")
        self.create_widget("Grid Widget 3", widget_type="grid")


class GetAllWidgetsTest(BaseViewTest):

    def test_get_all_widgets(self):
        """
        This test ensures that all widgets added in the setUp method
        exist when we make a GET request to the widgets/ endpoint
        """

        response = self.client.get(
            reverse(widgets, kwargs={"version": "v1"})
        )
        expected = Widget.objects.all()

        serialized = WidgetSerializer(expected, many=True)

        response_using_serializer = {
            'widget_query_count': len(serialized.data),
            'widgets': serialized.data
            }
        self.assertEqual(response.data, response_using_serializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_grid_widgets(self):
        """
        This test makes a GET request to the widgets/ endpoint
        using the widget_type filter set to 'grid'. It then checks
        that all returned widgets have the correct widget_type, and
        that the response body is the same whether using the endpoint
        or a serializer.
        """

        response = self.client.get(
            reverse(widgets, kwargs={"version": "v1",
                                     "widget_type": "grid"})
        )

        assert response.data.get('widgets')

        for w in response.data['widgets']:
            assert w['widget_type'] == 'grid'

        expected = Widget.objects.filter(widget_type="grid")
        serialized = WidgetSerializer(expected, many=True)

        response_using_serializer = {
            'widget_query_count': len(serialized.data),
            'widgets': serialized.data
            }

        self.assertEqual(response.data, response_using_serializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_widgets_and_get_single_widget(self):
        """
        This test ensures we can add a widget using a POST request,
        which is then retrievable using a GET request.
        """

        data = {"name": "new widget", "widget_type": "pieChart"}
        response = self.client.post(
            reverse(widgets, kwargs={"version": "v1"}),
            data,
            format="json"
        )

        new_id = response.data["added"]["id"]

        response = self.client.get(
            reverse(widget, kwargs={"version": "v1",
                                    "id": new_id})
        )

        expected = Widget.objects.filter(id=new_id)

        serialized = WidgetSerializer(expected, many=True)

        response_using_serializer = {
            'widget': serialized.data[0]
            }

        self.assertEqual(response.data, response_using_serializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_single_widget(self):
        """
        This test ensures we can edit a widget's data using a PUT
        request, which is then verified by using a GET request.
        """

        # First, verify widget with id 2 is of type heatMap:

        response = self.client.get(reverse(widget,
                                           kwargs={
                                               "version": "v1",
                                               "id": 2
                                            }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data.get("widget").get("id") == 2
        assert response.data.get("widget").get(
            "widget_type") == "heatMap"
        assert response.data.get("widget").get(
            "name") == "Heat Map Widget"

        # Change type of widget #2 to bubbleChart, and name to "Bubble
        # Chart Widget":

        data = {"name": "Bubble Chart Widget",
                "widget_type": "bubbleChart"}
        response = self.client.put(
            reverse(widget, kwargs={"version": "v1", "id": 2}),
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse(widget, kwargs={"version": "v1",
                                    "id": 2})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("widget").get("id"), 2)
        self.assertEqual(response.data.get("widget").get(
            "name"), "Bubble Chart Widget")
        self.assertEqual(response.data.get("widget").get(
            "widget_type"), "bubbleChart")

    def test_delete_single_widget(self):
        """
        This test ensures we can delete a widget using a DELETE
        request, which is then verified by using a GET request.
        """

        # First, verify widget with id 3 exists in database:

        response = self.client.get(
            reverse(widget, kwargs={"version": "v1",
                                    "id": 3})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("widget").get("id"), 3)

        # Delete widget #3:

        response = self.client.delete(
            reverse(widget, kwargs={"version": "v1", "id": 3}),
            format="json"
        )

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

        response = self.client.get(
            reverse(widget, kwargs={"version": "v1",
                                    "id": 3})
        )

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
        expected_response_body = {"Error": "Invalid Widget ID"}
        self.assertEqual(response.data, expected_response_body)
