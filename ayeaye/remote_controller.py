from typing import Dict, List
import json

import requests

from ayeaye.setting_loader import get_signal_settings, get_irkit_settings, get_server_settings


class RemoteController:

    def __init__(self, device_phrase2name, order_phrase2name, order_name2signal, irkit_settings, server_settings):
        self._device_phrase2name = device_phrase2name
        self._order_phrase2name = order_phrase2name
        self._order_name2signal = order_name2signal
        self._irkit_settings = irkit_settings
        self._server_settings = server_settings

    def run(self, posted_data):
        if posted_data['key'] != self._server_settings['key']:
            return dict(message='invalid key')
        return self._run(posted_data['text'])

    def _run(self, message):
        device_name = self._detect_device(message, self._device_phrase2name)
        order_name = self._detect_order(message, device_name, self._order_phrase2name)
        signal = self._extract_signal(device_name, order_name, self._order_name2signal)
        response = self._send_signal(signal, self._irkit_settings)
        return response

    @staticmethod
    def _detect_device(message, device_phrase2name):
        for device_phrase, device_name in device_phrase2name.items():
            if device_phrase in message:
                return device_name
        return None

    @staticmethod
    def _detect_order(message, device_name, order_phrase2name):
        if device_name not in order_phrase2name:
            return None
        for order_phrase, order_name in order_phrase2name[device_name].items():
            if order_phrase in message:
                return order_name
        return None

    @staticmethod
    def _extract_signal(device_name, order_name, order_name2signal):
        if device_name not in order_name2signal:
            return None

        if order_name not in order_name2signal[device_name]:
            return None

        return order_name2signal[device_name][order_name]

    @staticmethod
    def _send_signal(signal, irkit_settings):
        url = f'http://{format(irkit_settings["url"])}/messages'
        message = {'format': 'raw', 'freq': 38, 'data': signal}
        message = json.dumps(message)

        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'python',
        }

        r = requests.post(url, headers=headers, data=message)
        return r

    @classmethod
    def build(cls):
        signal_settings = get_signal_settings()
        device_phrase2name: Dict[str, str] = cls._build_device_phrase2name(signal_settings)
        order_phrase2name: Dict[str, Dict[str, str]] = cls._build_order_phrase2name(signal_settings)
        order_name2signal: Dict[str, Dict[str, List[int]]] = cls._build_order_name2signal(signal_settings)

        irkit_settings = get_irkit_settings()
        server_settings = get_server_settings()

        return cls(device_phrase2name, order_phrase2name, order_name2signal, irkit_settings, server_settings)

    @staticmethod
    def _build_device_phrase2name(signal_settings):
        device_phrase2name = {}
        for device_name, v in signal_settings.items():
            device_phrase2name.update({pat: device_name for pat in v['device_pattern']})
        return device_phrase2name

    @staticmethod
    def _build_order_phrase2name(signal_settings):
        order_phrase2name = {}
        for device_name, v in signal_settings.items():

            device_order_phrase2name = {}
            for order_name, order_value in v['orders'].items():
                device_order_phrase2name.update({pat: order_name for pat in order_value['pattern']})

            order_phrase2name[device_name] = device_order_phrase2name

        return order_phrase2name

    @staticmethod
    def _build_order_name2signal(signal_settings):
        order_name2signal = {}
        for device_name, v in signal_settings.items():

            device_order_name2signal = {}
            for order_name, order_value in v['orders'].items():
                device_order_name2signal[order_name] = order_value['signal']

            order_name2signal[device_name] = device_order_name2signal

        return order_name2signal
