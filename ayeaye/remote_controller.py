import os

import requests

from ayeaye.secret_loader import get_nature_remo_secret_token
from ayeaye.setting_loader import SignalSettings, make_signal_settings


class RemoteController:

    def __init__(self, signal_settings: SignalSettings, gcp_project_id: str, secret_id: str) -> None:
        self._signal_settings = signal_settings
        self._gcp_project_id = gcp_project_id
        self._secret_id = secret_id

    @classmethod
    def build(cls):
        datastore_namespace = os.environ['datastore_namespace']
        datastore_kind = os.environ['datastore_kind']
        datastore_id = os.environ['datastore_id']
        gcp_project_id = os.environ['gcp_project_id']
        secret_id = os.environ['secret_id']

        signal_settings = make_signal_settings(datastore_namespace, datastore_kind, datastore_id)
        return cls(signal_settings=signal_settings, gcp_project_id=gcp_project_id, secret_id=secret_id)

    def posted(self, posted_data):
        # TODO: user認証

        message = posted_data['text']

        device_name = self._detect_device(message)
        order_name = self._detect_order(message, device_name)
        signal_id = self._extract_signal_id(device_name, order_name)

        self._send_signal(signal_id=signal_id)
        return dict(message=f'succeeded signal_id={signal_id}')

    def _detect_device(self, message: str) -> str:
        for device_name, device_phrase_list in self._signal_settings.device_names.items():
            for device_phrase in device_phrase_list:
                if device_phrase in message:
                    return device_name
        raise ValueError(f'message `{message}` does not contain valid device phrase.')

    def _detect_order(self, message: str, device_name: str) -> str:
        order_names_dict = self._signal_settings.order_names[device_name]

        for order_name, order_phrase_list in order_names_dict.items():
            for order_phrase in order_phrase_list:
                if order_phrase in message:
                    return order_name
        raise ValueError(f'message `{message}` does not contain valid order phrase.')

    def _extract_signal_id(self, device_name: str, order_name: str):
        return self._signal_settings.order_signal[device_name][order_name]

    def _send_signal(self, signal_id: str):
        # TODO: ユーザーごとにsecret token切り替え
        nature_remo_secret_token = get_nature_remo_secret_token(gcp_project_id=self._gcp_project_id, secret_id=self._secret_id)

        url = f'https://api.nature.global/1/signals/{signal_id}/send'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {nature_remo_secret_token}',
        }

        requests.post(url, headers=headers)
