"""
Serializers transform incoming data into a format that can be used by
the Django app code, and then reconstruct it so the data can be sent
back out.
"""

from rest_framework import serializers
from .models import Widget


class WidgetSerializer(serializers.ModelSerializer):
    """Serializer class used for widgets. Used in views.py to process
    data going to/from the database.
    """
    class Meta:
        model = Widget
        fields = ['id', 'name', 'widget_type', 'parts_count',
                  'created_date', 'updated_date']
