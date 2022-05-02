import unittest
from unittest import mock

from google.cloud import datastore

from ayeaye.setting_loader import SignalSettings, make_signal_settings


class TestSignalSettings(unittest.TestCase):

    def test_make_signal_settings(self):

        device_names_entity = datastore.Entity()
        device_names_entity['device_name_1'] = ['dev1', 'デバイス1']

        order_names_entity = datastore.Entity()
        order_names_entity_inner_1 = datastore.Entity()
        order_names_entity_inner_1['turn_on'] = ['オン', 'つけて', '電源']
        order_names_entity['device_name_1'] = order_names_entity_inner_1

        order_signal_entity = datastore.Entity()
        order_signal_entity_inner_1 = datastore.Entity()
        order_signal_entity_inner_1['turn_on'] = 'signal_pattern_1'
        order_signal_entity['device_name_1'] = order_signal_entity_inner_1

        datastore_entity = datastore.Entity()
        datastore_entity['device_names'] = device_names_entity
        datastore_entity['order_names'] = order_names_entity
        datastore_entity['order_signal'] = order_signal_entity

        with mock.patch('ayeaye.setting_loader._load_datastore_entity', return_value=datastore_entity):
            resulted = make_signal_settings(datastore_namespace='test', datastore_kind='test', datastore_id='test')
            expected = SignalSettings(
                device_names={'device_name_1': ['dev1', 'デバイス1']},
                order_names={'device_name_1': {
                    'turn_on': ['オン', 'つけて', '電源']
                }},
                order_signal={'device_name_1': {
                    'turn_on': 'signal_pattern_1'
                }},
            )
            self.assertEqual(resulted, expected)
