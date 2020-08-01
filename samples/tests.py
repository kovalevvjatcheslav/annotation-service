from collections import OrderedDict
from django.test import TestCase
from samples.serializers import SampleSerializer
from samples import models
import json


class DummyValue:
    def __eq__(self, other):
        return True


class APITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.maxDiff = None

    def test_create_image_with_label(self):
        label_meta = {'confirmed': False, 'confidence_percent': 0.9}
        shape = {'start_x': 10.0, 'start_y': 20.0, 'end_x': 30.0, 'end_y': 40.0}
        label = {'label_meta': label_meta, 'shape': shape, 'class_id': 'tooth', 'surface': 'BOL'}
        image_name = 'test_image.jpeg'
        with open(f'samples/test_data/{image_name}', 'rb') as image:
            resp = self.client.post('/api/sample/', data={'image': image, 'label': json.dumps(label)})
        self.assertEqual(resp.status_code, 200)
        label_meta.update({'id': DummyValue()})
        shape.update({'id': DummyValue()})
        label.update({'id': DummyValue()})
        serialized_sample = {'id': DummyValue(), 'label': label, 'image_name': image_name}
        sample = models.Sample.objects.all()[0]
        self.assertEqual(serialized_sample, self.__ordered_dict_to_dict(dict(SampleSerializer(sample).data)))
        self.assertEqual(sample.id, resp.data)

    @classmethod
    def __ordered_dict_to_dict(cls, data):
        result = {}
        for key, value in data.items():
            if isinstance(value, OrderedDict):
                result.update({key: cls.__ordered_dict_to_dict(value)})
            else:
                result.update({key: value})
        return result
