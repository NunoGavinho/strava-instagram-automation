import requests
import json
import os

def load_strava_credentials():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config["strava"]

def refresh_access_token():
    credentials = load_strava_credentials()
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"],
        "refresh_token": credentials["refresh_token"],
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        # Atualiza o arquivo config.json
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        config["strava"]["access_token"] = token_data["access_token"]
        config["strava"]["refresh_token"] = token_data["refresh_token"]
        config["strava"]["expires_at"] = token_data["expires_at"]
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)
        print("Access token successfully refreshed!")
        return token_data["access_token"]
    else:
        print(f"Failed to refresh token: {response.status_code}")
        print(response.text)
        return None

def fetch_activities():
    credentials = load_strava_credentials()
    access_token = credentials["access_token"]
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 401:  # Token expirado
        print("Access token expired. Refreshing...")
        access_token = refresh_access_token()
        if not access_token:
            return []
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar atividades: {response.status_code}")
        print(response.text)
        return []

if __name__ == "__main__":
    print("Fetching activities...")
    activities = fetch_activities()
    print(f"Fetched {len(activities)} activities.")

