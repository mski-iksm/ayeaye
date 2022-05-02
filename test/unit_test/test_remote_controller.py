import unittest
from unittest.mock import patch

from ayeaye.remote_controller import RemoteController
from ayeaye.setting_loader import SignalSettings


class TestRemoteController(unittest.TestCase):

    def test_posted(self):
        with patch('requests.post'):
            with patch('ayeaye.remote_controller.get_nature_remo_secret_token', return_value='test_token'):
                signal_settings = SignalSettings(
                    device_names={'device_name_1': ['dev1', 'デバイス1']},
                    order_names={'device_name_1': {
                        'turn_on': ['オン', 'つけて', '電源']
                    }},
                    order_signal={'device_name_1': {
                        'turn_on': 'signal_pattern_1'
                    }},
                )
                remote_controller = RemoteController(signal_settings=signal_settings, gcp_project_id='test', secret_id='test')
                posted_data = {'text': 'デバイス1をつけて'}
                resulted = remote_controller.posted(posted_data=posted_data)
                expected = dict(message='succeeded signal_id=signal_pattern_1')
                self.assertEqual(resulted, expected)
