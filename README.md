# ayeaye
<<概要>>

## 設定方法

## サーバー側起動方法
```bash
export datastore_namespace=XXXXXXXXXXXXX
export datastore_kind=XXXXXXXXXXXXX
export datastore_id=XXXXXXXXXXXXX
export gcp_project_id=XXXXXXXXXXXXX
export secret_id=XXXXXXXXXXXX

python run_server.py --port-number=<port-number>
```

## リモコン操作方法
```bash
curl -X GET "https://api.nature.global/1/appliances/{appliances_id}/signals" -H "accept: application/json" -H "Authorization: Bearer {nature_remo_token}"
```

