import json
from rest_framework import renderers


class InternalRenderer(renderers.BaseRenderer):
    media_type = 'multipart/form-data'
    format = 'internal'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps(data)


class ExportRenderer(renderers.BaseRenderer):
    media_type = 'multipart/form-data'
    format = 'export'

    def render(self, data, media_type=None, renderer_context=None):
        data.pop('label_meta', None)
        data.pop('shape', None)
        return json.dumps(data)
