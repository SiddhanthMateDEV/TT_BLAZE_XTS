import socketio.client
from config.product_config.main import ProductConfig
from config.route_config.main import RouteConfig
from subscribe.main import SubscribedInstruments
from xts_message_codes.main import XtsMessageCodes

import asyncio
from urllib.parse import urljoin
import requests as rqs
import json 
import socketio
from pymongo import MongoClient
import redis 
from itertools import product
import aiohttp

class WebSocket(ProductConfig,RouteConfig,SubscribedInstruments,XtsMessageCodes):
    def __init__(self,
                 root_url = "https://ttblaze.iifl.com",
                 mongo_uri = "mongodb://localhost:27017",
                 user_id = None,
                 token = None,
                 db_name = None,
                 coll_name = None,
                 exchange_segment = None,
                 intrument_id = None,
                 publish_format = "JSON",
                 broadcast_mode = "Full",
                 socket_path = "/apimarketdata/socket.io"
                 ):
        if not all([root_url,token,db_name,coll_name,publish_format,broadcast_mode,]):
            raise ValueError("Fields required for initiating a websocket are empty or None")

        self.root_url = root_url
        self.token = token
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[str(db_name)]
        self.mongo_coll = self.mongo_db[str(coll_name)]
        self.publish_format = publish_format
        self.broadcast_mode = broadcast_mode
        self.socket_path = socket_path
        self.socket = socketio.Client()
        self.event_loop = asyncio.get_event_loop()

        super().__init__()

        if not all([self._routes, self.products]):
            raise ValueError("Empty Config fields for routes and products")


    async def _request(self, route = None, method_req = None, 
                       parameters = None, pool = None):
        params = parameters or {}
        try:
            uri = self._routes[str(route)].format(**params)
            url = urljoin(self.root_url, uri)
        except KeyError as e:
            raise ValueError(f"Key error for self._routes: {route}")
        headers = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method = method_req,
                    url = url,
                    json = params if method_req in ["POST","PUT"] else None,
                    params = params if method_req in ["GET","DELETE"] else None,
                    headers = headers,
                    ssl = True
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except rqs.exceptions.RequestException as e:
                raise ValueError(fr"HTTPS Error occured at _request function, Error Code: {e.response.status_code}")
            except json.JSONDecodeError as e:
                raise ValueError("Failed to load JSON response") from e
            except Exception as e:
                raise ValueError("Error occured in _request function") from e
        
    async def _post(self, route_param = None, params = None):
        return await self._request(route = route_param, method_req = "POST", parameters = params, pool = None)
    
    async def send_subscription(self, instruments = None, xts_message_codes = None):
        try:
            responses = []
            for instrument, code in product(instruments,xts_message_codes):
                params_code = {
                    'instruments': instrument,
                    'xtsMessageCode': code,
                }
                response = await self._post(route_param = 'market.instruments.subscription', params = params_code)
                responses.append(response)
            return responses
        except Exception as e:
            raise ValueError("Error in sending subscription") from e
        
    async def subscribe_to_codes(self):
        response = await self.send_subscription(instruments = self.subscribe_payload, xts_message_codes = self.xts_message_codes)
        return response


    def socket_functions(self):
        @self.socket.event
        def connect():
            print("Connected to the server")

    

    
    
    

        




    
        