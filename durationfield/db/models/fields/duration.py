# -*- coding: utf-8 -*-
from datetime import timedelta
from durationfield.forms.fields import DurationField as FDurationField
from django.db.models.fields import Field
from django.core.exceptions import ValidationError
from django.db import connection
from django.utils import timestring

class DurationField(Field):
    def __init__(self, *args, **kwargs):
        super(DurationField, self).__init__(*args, **kwargs)
        self.max_digits, self.decimal_places = 20, 6

    def get_internal_type(self):
        return "BigIntegerField"

    def get_db_prep_save(self, value):
        if value is None:
            return None # db NULL
        if isinstance(value, int) or isinstance(value, long):
            value = timedelta(microseconds=value)
        return value.days * 24 * 3600 * 1000000 + value.seconds * 1000000 + value.microseconds

    def to_python(self, value):
        return value

    def formfield(self, form_class=FDurationField, **kwargs):
        return super(DurationField, self).formfield(form_class, **kwargs)
