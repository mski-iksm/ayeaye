import google_crc32c
from google.cloud import secretmanager


def get_nature_remo_secret_token(gcp_project_id: str, secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{gcp_project_id}/secrets/{secret_id}/versions/latest'
    response = client.access_secret_version(request={"name": name})

    # Verify payload checksum.
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        raise ValueError('Data corruption detected.')

    return response.payload.data.decode('UTF-8')
