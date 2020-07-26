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


class SampleSerializer(serializers.ModelSerializer):
    label = LabelSerializer()

    class Meta:
        model = Sample
        fields = '__all__'
