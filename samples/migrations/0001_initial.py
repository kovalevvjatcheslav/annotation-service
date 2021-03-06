# Generated by Django 3.0.8 on 2020-07-26 08:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('class_id', models.CharField(default='tooth', max_length=100)),
                ('surface', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='LabelMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('confidence_percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_x', models.FloatField()),
                ('start_y', models.FloatField()),
                ('end_x', models.FloatField()),
                ('end_y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_name', models.CharField(max_length=100, unique=True)),
                ('label', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='samples.Label')),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='label_meta',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='samples.LabelMeta'),
        ),
        migrations.AddField(
            model_name='label',
            name='shape',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='samples.Shape'),
        ),
    ]
