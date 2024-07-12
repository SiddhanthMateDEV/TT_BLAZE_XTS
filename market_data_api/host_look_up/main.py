import requests as rqs
import json 
from configparser import ConfigParser

class host_look_up:
    def __init__(self, url = "https://ttblaze.iifl.com", 
                 access_password = "2021HostLookUpAccess",
                 version = "interactive_1.0.1",
                 secretKey = None,
                 apiKey = None
                 ):
        self.url = url
        self.access_password = access_password
        self.version = version
        self.secretKey = secretKey
        self.apiKey = apiKey
        self.auth_token = None
        self.token = None
        self.exchangeSegment = None
        self.xtsMessageCode = None
        self.publishFormat = None
        self.broadCastMode = None
        self.instrumentType = None
        self.index_list_cash_market = None
        self.config = ConfigParser()
        self.series_futures_options_list = None

    def host_look_up(self):
        HOST_LOOKUP_URL = fr"{self.url}:4000/HostLookUp"
        payload_host_lookup = {
            "accesspassword": self.access_password,
            "version": self.version
        }
        response = rqs.post(url = HOST_LOOKUP_URL, json = payload_host_lookup)
        if response.status_code == 200:
            unique_key = response.json().get('result').get('uniqueKey') 
            if unique_key is None:
                raise ValueError("uniqueKey genereated in empty")
            else:
                self.auth_token = unique_key
                self.config['AUTH'] = {'unique_key': unique_key}
                with open("TT_BLAZE_XTS/market_data_api/data/xts_login.ini",'w') as configfile:
                    self.config.write(configfile)
        else:
            print(fr"HOST LOOKUP REQUEST HAS FAILED")

    def login_market_api(self):
        payload_market_data = {
            "secretKey": self.secretKey,
            "appKey": self.apiKey,
            "source": "WebAPI"
        }
        login_header_market_data = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }
        LOGIN_URL_MARKET_API = fr"{self.url}/apimarketdata/auth/login"
        response_market_data_login = rqs.post(url = LOGIN_URL_MARKET_API, headers = login_header_market_data, json = payload_market_data)
        if response_market_data_login.status_code == 200:
            login_response = response_market_data_login.json()
            self.token = login_response.get('result').get('token')
            self.config['AUTH'].update({'token': self.token})
            with open("TT_BLAZE_XTS/market_data_api/data/xts_login.ini",'w') as configfile:
                self.config.write(configfile)
            return login_response
        else:
            print("LOGIN INTO MARKET DATA API FAILED")
    
    def client_config_response(self):
        #client config
        CLIENT_CONFIG_URL = fr"{self.url}/apimarketdata/config/clientConfig"
        header_client_config = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }
        response_client_config = rqs.get(url = CLIENT_CONFIG_URL, headers = header_client_config)
        if response_client_config.status_code == 200:
            client_config_response_data = response_client_config.json()
            # this might cause an error if so check the key name and change it
            self.exchangeSegment = client_config_response_data.get('exchangeSegments') 
            self.xtsMessageCode = client_config_response_data.get('xtsMessageCode') 
            self.publishFormat = client_config_response_data.get('publishFormat') 
            self.broadCastMode = client_config_response_data.get('broadCastMode') 
            self.instrumentType = client_config_response_data.get('instrumentType') 
        else:
            print("CLIENT CONFIG REQUEST FAILED")

    #get index list
    def index_list_response(self):
        INDEX_LIST_URL = fr"{self.url}/apimarketdata/instruments/indexlist"
        header_index_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }
        payload_index_list = {
            'exchangeSegment': 1
        }
        response_index_list = rqs.get(url = INDEX_LIST_URL, headers = header_index_list, params = payload_index_list)
        if response_index_list.status_code == 200:
            index_list_data = response_index_list.json() 
            self.index_list_cash_market = index_list_data.get('result').get('indexList')
        else:
            print("BAD INDEX LIST REQUEST")

    #get series list
    def series_list(self):
        SERIES_LIST_URL = fr"{self.url}/apimarketdata/instruments/instrument/series"
        header_series_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }
        payload_series_list = {
            'exchangeSegment': 2
        }

        response_series_list = rqs.get(url = SERIES_LIST_URL, headers = header_series_list, params = payload_series_list)

        if response_series_list.status_code == 200:
            series_list_data = response_series_list.json()
            self.series_futures_options_list = series_list_data.get('result')
        else:
            print("BAD REQUEST SERIES LIST")

    def options_expiry_list(self, series = None, symbol = None):
        OPTIONS_EXPIRY_LIST_URL = "https://ttblaze.iifl.com/apimarketdata/instruments/instrument/expiryDate"
        
        header_option_expiry_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }

        payload_option_expiry_list = {
            'exchangeSegment': 2,
            'series': str(series),
            'symbol': str(symbol)
        }

        response_series_list = rqs.get(url = OPTIONS_EXPIRY_LIST_URL, headers = header_option_expiry_list, params = payload_option_expiry_list)

        if response_series_list.status_code == 200:
            series_list_data = response_series_list.json()
            return series_list_data
        else:
            print("BAD REQUEST SERIES LIST")
    
 
