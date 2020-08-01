from django.db import transaction
from rest_framework import serializers
from samples.models import LabelMeta, Shape, Label, Sample


class LabelMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelMeta
        fields = '__all__'


class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shape
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    label_meta = LabelMetaSerializer()
    shape = ShapeSerializer()

    class Meta:
        model = Label
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        label_meta = LabelMetaSerializer().create(validated_data.get('label_meta'))
        shape = ShapeSerializer().create(validated_data.get('shape'))
        validated_data.update({'label_meta': label_meta, 'shape': shape})
        return super().create(validated_data)


class SampleSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = Sample
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        label = LabelSerializer().create(validated_data.get('label'))
        validated_data.update({'label': label})
        return super().create(validated_data)
