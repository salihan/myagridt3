import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import requests
from io import StringIO

class HomeModel2:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = Credentials.from_service_account_file('models/keyfile.json', scopes=scopes)
        gc = gspread.authorize(credentials)

        self.session = requests.Session()

        self.actual_data_url = 'https://docs.google.com/spreadsheets/d/1WKOfNmt9KYKDHxaR3c_uO3YSTpYzzup85Wsde5OkTic/gviz/tq?tqx=out:csv&gid=0'

        # Load data or download and cache if not available
        self.actual_data = self.load_data(self.actual_data_url)

    def load_data(self, url):
        # Check if data is already cached in the session
        if url in self.session.adapters:
            response = self.session.get(url)
            if response.status_code == 200:
                data = pd.read_csv(StringIO(response.text))
                return data
            else:
                print(f"Failed to fetch data from Google Sheets. Status code: {response.status_code}")
                return None

        # If not cached, download data from Google Sheets and cache it
        response = self.session.get(url)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            return data
        else:
            print(f"Failed to fetch data from Google Sheets. Status code: {response.status_code}")
            return None

    def get_actual_data(self):
        return self.actual_data
