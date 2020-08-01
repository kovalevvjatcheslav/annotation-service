import json
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from samples.serializers import LabelSerializer, SampleSerializer


class SampleView(APIView):
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        sample_serializer = SampleSerializer(data={'label': json.loads(request.data.get('label')),
                                                   'image_name': image.name})
        if not sample_serializer.is_valid():
            return Response(sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            sample = sample_serializer.save()
            default_storage.save(name=image.name, content=image)
        return Response(sample.id)
