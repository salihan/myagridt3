import requests

BASE_URL = "https://api.satu.singularityaero.tech"
API_KEY = "25|iEjCopmkc73ZFYtCzHCFLnCJb670ErvV3VBfGCt2"  # Replace with your actual API key

def get_telemetries(device_unique_id, telemetry_type_code=None, date_start=None, date_end=None):
    url = f"{BASE_URL}/api/telemetries"

    print(device_unique_id, telemetry_type_code, date_start, date_end)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    params = {
        "deviceUniqueId": device_unique_id,
        "telemetryTypeCode": telemetry_type_code,
        "dateStart": date_start,
        "dateEnd": date_end,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        return None  # Handle the error as needed
