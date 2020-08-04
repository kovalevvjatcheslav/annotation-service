import json
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import FileResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from samples.serializers import LabelSerializer, SampleSerializer
from samples.models import Sample, Label
from samples.renderers import ExportRenderer, InternalRenderer


class SampleView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        if image is None:
            return Response({'image': ['Must not be empty.']}, status=status.HTTP_400_BAD_REQUEST)
        data = {'image_name': image.name}
        label = request.data.get('label')
        if label:
            data.update({'label': json.loads(label)})
        sample_serializer = SampleSerializer(data=data)
        if not sample_serializer.is_valid():
            return Response(sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            sample = sample_serializer.save()
            default_storage.save(name=image.name, content=image)
            return Response(sample.id, content_type='application/json')


class LabelView(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [ExportRenderer, InternalRenderer]

    def get(self, request, label_id=None, *args, **kwargs):
        if label_id:
            label = Label.objects.get(id=label_id)
            label_serializer = LabelSerializer(label)
        else:
            label_serializer = LabelSerializer(Label.objects.all(), many=True)
        return Response(label_serializer.data, content_type='application/json')

    def put(self, request, label_id, *args, **kwargs):
        label_data = request.data.get('label')
        if label_data is None:
            return Response({'label': ['Must not be empty.']}, status=status.HTTP_400_BAD_REQUEST)
        label = Label.objects.get(id=label_id)
        label_serializer = LabelSerializer(label, data=json.loads(label_data), partial=True)
        if not label_serializer.is_valid():
            return Response(label_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            label_serializer.save()
            return Response(label_serializer.data, content_type='application/json')


class ImageView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, image_name, *args, **kwargs):
        if not default_storage.exists(image_name):
            return Response({'image_name': ['Does not exist.']}, status=status.HTTP_400_BAD_REQUEST)
        return FileResponse(default_storage.open(name=image_name))
