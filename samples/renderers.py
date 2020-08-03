import json
from collections import Mapping
from rest_framework import renderers
from rest_framework.utils.serializer_helpers import ReturnList


class InternalRenderer(renderers.BaseRenderer):
    media_type = 'multipart/form-data'
    format = 'internal'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps(data)


class ExportRenderer(renderers.BaseRenderer):
    media_type = 'multipart/form-data'
    format = 'export'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, Mapping):
            data.pop('label_meta', None)
            data.pop('shape', None)
        elif isinstance(data, ReturnList):
            for each in data:
                each.pop('label_meta', None)
                each.pop('shape', None)
        return json.dumps(data)
