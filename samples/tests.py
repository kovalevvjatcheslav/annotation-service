import shutil
from collections import OrderedDict
from django.test import TestCase, override_settings
from samples.serializers import SampleSerializer, LabelSerializer
from samples.models import Sample, Label
import json


class DummyValue:
    def __eq__(self, other):
        return True


@override_settings(MEDIA_ROOT='test/media/')
class APITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.maxDiff = None

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
        try:
            shutil.rmtree('test/media')
        except Exception as ex:
            print(ex)

    def test_create_sample_with_label(self):
        image_name = 'test_image.jpeg'
        label_meta = {'confirmed': False, 'confidence_percent': 0.9}
        shape = {'start_x': 10.0, 'start_y': 20.0, 'end_x': 30.0, 'end_y': 40.0}
        label = {'label_meta': label_meta, 'shape': shape, 'class_id': 'tooth', 'surface': 'BOL'}
        with open(f'samples/test_data/{image_name}', 'rb') as image:
            resp = self.client.post('/api/sample/', data={'image': image, 'label': json.dumps(label)})
        self.assertEqual(resp.status_code, 200)
        label_meta.update({'id': DummyValue()})
        shape.update({'id': DummyValue()})
        label.update({'id': DummyValue()})
        serialized_sample = {'id': DummyValue(), 'label': label, 'image_name': image_name}
        sample = Sample.objects.all()[0]
        self.assertEqual(serialized_sample, self.__ordered_dict_to_dict(dict(SampleSerializer(sample).data)))

    def test_create_sample_without_label(self):
        image_name = 'test_image.jpeg'
        with open(f'samples/test_data/{image_name}', 'rb') as image:
            resp = self.client.post('/api/sample/', data={'image': image})
        self.assertEqual(resp.status_code, 200)
        sample = Sample.objects.all()[0]
        serialized_sample = {'id': DummyValue(), 'label': None, 'image_name': image_name}
        self.assertEqual(serialized_sample, dict(SampleSerializer(sample).data))

    def test_create_sample_empty_query(self):
        resp = self.client.post('/api/sample/')
        self.assertEqual(resp.status_code, 400)
        expected_data = {'image': ['Must not be empty.']}
        self.assertEqual(expected_data, json.loads(resp.content))

    def test_create_sample_wrong_params(self):
        image_name = 'test_image.jpeg'
        label_meta = {'confirmed': -0.5, 'confidence_percent': -1}
        shape = {'start_x': 'test', 'start_y': 'test', 'end_x': 'test', 'end_y': 'test'}
        label = {'label_meta': label_meta, 'shape': shape, 'class_id': False, 'surface': -1}
        with open(f'samples/test_data/{image_name}', 'rb') as image:
            resp = self.client.post('/api/sample/', data={'image': image, 'label': json.dumps(label)})
        expected_data = {
            'label': {'label_meta': {'confirmed': ['Must be a valid boolean.'],
                                     'confidence_percent': ['Ensure this value is greater than or equal to 0.']},
                      'shape': {'start_x': ['A valid number is required.'], 'start_y': ['A valid number is required.'],
                                'end_x': ['A valid number is required.'], 'end_y': ['A valid number is required.']},
                      'class_id': ['Not a valid string.']}
        }
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(expected_data, json.loads(resp.content))

    def test_get_internal_label(self):
        image_name = 'test_image.jpeg'
        label_meta = {'confirmed': False, 'confidence_percent': 0.9}
        shape = {'start_x': 10.0, 'start_y': 20.0, 'end_x': 30.0, 'end_y': 40.0}
        label_data = {'label_meta': label_meta, 'shape': shape, 'class_id': 'tooth', 'surface': 'BOL'}
        sample_serializer = SampleSerializer(data={'label': label_data, 'image_name': image_name})
        sample_serializer.is_valid()
        sample = sample_serializer.save()
        resp = self.client.get(f'/api/label/{sample.id}/', data={'format': 'internal'})
        self.assertEqual(resp.status_code, 200)
        label_meta.update({'id': DummyValue()})
        shape.update({'id': DummyValue()})
        label_data.update({'id': DummyValue()})
        self.assertEqual(label_data, json.loads(resp.content))

    def test_get_export_label(self):
        image_name = 'test_image.jpeg'
        label_meta = {'confirmed': False, 'confidence_percent': 0.9}
        shape = {'start_x': 10.0, 'start_y': 20.0, 'end_x': 30.0, 'end_y': 40.0}
        label_data = {'label_meta': label_meta, 'shape': shape, 'class_id': 'tooth', 'surface': 'BOL'}
        sample_serializer = SampleSerializer(data={'label': label_data, 'image_name': image_name})
        sample_serializer.is_valid()
        sample = sample_serializer.save()
        resp = self.client.get(f'/api/label/{sample.id}/', data={'format': 'export'})
        self.assertEqual(resp.status_code, 200)
        label_data.update({'id': DummyValue()})
        label_data.pop('label_meta')
        label_data.pop('shape')
        self.assertEqual(label_data, json.loads(resp.content))

    def test_get_label(self):
        image_name = 'test_image.jpeg'
        label_meta = {'confirmed': False, 'confidence_percent': 0.9}
        shape = {'start_x': 10.0, 'start_y': 20.0, 'end_x': 30.0, 'end_y': 40.0}
        label_data = {'label_meta': label_meta, 'shape': shape, 'class_id': 'tooth', 'surface': 'BOL'}
        sample_serializer = SampleSerializer(data={'label': label_data, 'image_name': image_name})
        sample_serializer.is_valid()
        sample = sample_serializer.save()
        resp = self.client.get(f'/api/label/{sample.id}/')
        self.assertEqual(resp.status_code, 200)
        label_data.update({'id': DummyValue()})
        label_data.pop('label_meta')
        label_data.pop('shape')
        self.assertEqual(label_data, json.loads(resp.content))

    def test_update_label(self):
        image_name = 'test_image.jpeg'
        label_meta = {'confirmed': False, 'confidence_percent': 0.9}
        shape = {'start_x': 10.0, 'start_y': 20.0, 'end_x': 30.0, 'end_y': 40.0}
        label_data = {'label_meta': label_meta, 'shape': shape, 'class_id': 'tooth', 'surface': 'BOL'}
        sample_serializer = SampleSerializer(data={'label': label_data, 'image_name': image_name})
        sample_serializer.is_valid()
        sample = sample_serializer.save()
        sample_serializer.update()


    @classmethod
    def __ordered_dict_to_dict(cls, data):
        result = {}
        for key, value in data.items():
            if isinstance(value, OrderedDict):
                result.update({key: cls.__ordered_dict_to_dict(value)})
            else:
                result.update({key: value})
        return result
