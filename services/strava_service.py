import requests
import json
import os


def load_strava_credentials():


    return {
        "client_id": "144986",
        "client_secret": "2e7837b1af58f0a4b0ee2d298b91386e510b1b7b",
        "access_token": "07e2dd5d425570daab1719538e61c13afb64da6d",
        "refresh_token": "ba30628ccb4d05be9ec696b5435f8b090e054c55"
    }


def refresh_access_token():

    credentials = load_strava_credentials()
    client_id = credentials["client_id"]
    client_secret = credentials["client_secret"]
    refresh_token = credentials["refresh_token"]

    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        token_data = response.json()


        credentials["access_token"] = token_data["access_token"]
        credentials["refresh_token"] = token_data["refresh_token"]

        print("Access token successfully refreshed!")
        return token_data["access_token"]
    else:
        print(f"Failed to refresh access token: {response.status_code}")
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

    if response.status_code == 401:  # Token inválido ou expirado
        print("Access token expired. Refreshing...")
        access_token = refresh_access_token()
        if not access_token:
            print("Could not refresh access token. Exiting.")
            return []

        # Retry the request with the new access token
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        activities = response.json()
        return activities
    else:
        print(f"Erro ao buscar atividades: {response.status_code}")
        print(response.text)
        return []


if __name__ == "__main__":
    activities = fetch_activities()
    print(f"Fetched {len(activities)} activities.")
