import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import requests
from io import StringIO  # Import StringIO from the io module

class PakchoiModel:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = Credentials.from_service_account_file('models/keyfile.json', scopes=scopes)
        gc = gspread.authorize(credentials)

        self.cached_responses = {}  # Dictionary to store cached responses

        # Open each of the spreadsheets by their respective URL
        self.actual_data_url = 'https://docs.google.com/spreadsheets/d/1ICcPbmdOCSE3lkpxFSQJLI1c-Lo6i0YadpeWfM4hhdw/gviz/tq?tqx=out:csv&gid=0'
        self.target_data_url = 'https://docs.google.com/spreadsheets/d/1MYeJfwp2l4e79Dn0bcWPYIwHQ5zXXIFT7zozSnwW8w0/gviz/tq?tqx=out:csv&gid=0'
        self.prediction_data_url = 'https://docs.google.com/spreadsheets/d/1mCd6hP5A1I-7pwhU-dqKTkMWGKr6Z47Akz8935YlnNI/gviz/tq?tqx=out:csv&gid=0'

        # Load data or download and cache if not available
        self.actual_data = self.load_data(self.actual_data_url)
        self.target_data = self.load_data(self.target_data_url)
        self.prediction_data = self.load_data(self.prediction_data_url)

    def load_data(self, url):
        # Check if data is already cached in the dictionary
        if url in self.cached_responses:
            return pd.read_csv(StringIO(self.cached_responses[url].text))

        # If not cached, download data from Google Sheets and cache it
        response = requests.get(url)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            self.cached_responses[url] = response  # Cache the response in the dictionary
            return data
        else:
            print(f"Failed to fetch data from Google Sheets. Status code: {response.status_code}")
            return None

    def get_actual_data(self):
        return self.actual_data

    def get_target_data(self):
        return self.target_data

    def get_prediction_data(self):
        return self.prediction_data
