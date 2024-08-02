
# XTS Functionality for TT Blaze API


This repository contains the implementation of the TT Blaze Market Data API using Python. 

The API provides real-time stock market data, instrument subscriptions, market depth events, candle data, open interest events, and more.

## Folder Structure

### 1. 'market_data_api' Directory

- `config`: Contains the two folders one for the config of products distributed by xts and the other is routes, which contains the paths for getting different api related backend functionality.
- `login`: Manages host look up and login to obtain authetication token and the token for each session.
- `market_data_api`: Provides example usage of the Market Data functionalities.
- `subscribe`: This contains a list of dictionaries of the exchange segment and instrument of id for whose id data will be subscribed.
- `web_socket`: Initializes the websocket instance to listen for data packets.
- `xts_message_codes`: Contains a list of all the codes of xts market data events.


## Documentation
- [Documentation](https://ttblaze.iifl.com/doc/marketdata/)

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/siddhanth-mate-9b0127222/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/SiddhanthMate)
