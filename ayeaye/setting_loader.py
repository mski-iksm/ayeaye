import dataclasses
from typing import Dict, List, Tuple

import yaml
from google.cloud import datastore


@dataclasses.dataclass
class RemoSettings:
    key: str


def make_remo_settings():
    pass


@dataclasses.dataclass
class SignalSettings:
    device_names: Dict[str, List[str]]
    order_names: Dict[str, Dict[str, List[str]]]
    order_signal: Dict[str, Dict[str, str]]


def _load_datastore_entity(datastore_namespace: str, datastore_kind: str, datastore_id: str) -> datastore.entity.Entity:
    client = datastore.Client(namespace=datastore_namespace)
    key = client.key(datastore_kind, datastore_id)
    return client.get(key)


def _load_device_names_from_datastore(datastore_entity: datastore.entity.Entity) -> Dict[str, List[str]]:
    device_names_entity = datastore_entity['device_names']
    return dict(device_names_entity.items())


def _load_order_names_from_datastore(datastore_entity: datastore.entity.Entity) -> Dict[str, Dict[str, List[str]]]:
    order_names_entity = datastore_entity['order_names']
    return {k: dict(v) for k, v in dict(order_names_entity.items()).items()}


def _load_order_signal_from_datastore(datastore_entity: datastore.entity.Entity) -> Dict[str, Dict[str, str]]:
    order_signal_entity = datastore_entity['order_signal']
    return {k: dict(v) for k, v in dict(order_signal_entity.items()).items()}


def make_signal_settings(datastore_namespace: str, datastore_kind: str, datastore_id: str) -> SignalSettings:
    datastore_entity = _load_datastore_entity(datastore_namespace=datastore_namespace, datastore_kind=datastore_kind, datastore_id=datastore_id)

    device_names = _load_device_names_from_datastore(datastore_entity=datastore_entity)
    order_names = _load_order_names_from_datastore(datastore_entity=datastore_entity)
    order_signal = _load_order_signal_from_datastore(datastore_entity=datastore_entity)

    return SignalSettings(device_names=device_names, order_names=order_names, order_signal=order_signal)
