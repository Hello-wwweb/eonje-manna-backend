import requests


class NaverMapAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = "lk4pjn6bhn"
        self.client_secret = "2HEO59y2raSXxjv1uH1MQVg7ptl5qXbKuoSUbWds"
        self.endpoint = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

    def reverse_geocode(self, latitude, longitude):
        url = self.endpoint
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
        }
        params = {
            "coords": f"{longitude},{latitude}",
            "output": "json",
            "orders": "addr,roadaddr",
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Failed to fetch data",
                "status_code": response.status_code,
            }

    def place_search(self, query):
        url = f"{self.endpoint}?coords={coords}&output={output}&orders={orders}"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
        }
        params = {
            "query": query,
            "coordinate": f"{longitude},{latitude}" if latitude and longitude else None,
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Failed to fetch data with status code {response.status_code}",
                "response_text": response.text,
                "status_code": response.status_code,
            }
