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
curl -X POST -H "Content-Type: application/json" -d '{"text":"テレビをつけて"}' https://0.0.0.0:7888/incoming --insecure
```

