"""This file stores models, which are Python objects used to access and
modify data inside the database.
"""

from django.db import models

from .env import WIDGET_TYPES


class Widget(models.Model):
    """Used to write to and read data in database.
    """
    name = models.CharField(max_length=64)
    parts_count = models.IntegerField(default=1)
    # author is writeable but not readable through the endpoints:
    author = models.CharField(max_length=32,
                              default='backend_dev')
    widget_type = models.CharField(max_length=32,
                                   choices=WIDGET_TYPES,
                                   default='unspecifiedType')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str():
        return self.name
