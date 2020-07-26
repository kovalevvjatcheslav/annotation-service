from uuid import uuid4
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class LabelMeta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    confirmed = models.BooleanField(default=False)
    confidence_percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])


class Shape(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    start_x = models.FloatField()
    start_y = models.FloatField()
    end_x = models.FloatField()
    end_y = models.FloatField()


class Label(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    label_meta = models.OneToOneField(LabelMeta, on_delete=models.SET_NULL, null=True)
    class_id = models.CharField(max_length=100, default='tooth')
    surface = models.CharField(max_length=3)
    shape = models.OneToOneField(Shape, on_delete=models.SET_NULL, null=True)


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image_name = models.CharField(max_length=100, unique=True)
    label = models.OneToOneField(Label, on_delete=models.SET_NULL, null=True)
