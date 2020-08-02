import json
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from samples.serializers import LabelSerializer, SampleSerializer
from samples.models import Sample
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
        return Response(sample.id)


class LabelView(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [ExportRenderer, InternalRenderer]

    def get(self, request, sample_id, *args, **kwargs):
        label = Sample.objects.get(id=sample_id).label
        return Response(LabelSerializer(label).data)

    # def put(self, request, sample_id, *args, **kwargs):
    #     pass
