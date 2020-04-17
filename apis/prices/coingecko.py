from common.http import request
from common.utilities.helper import Helper

import datetime as dt
import config.prices as cfg

import math


class CoinGecko:
    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()

        self.get_coins_list()

        # self.compute_financials()

        # self.get_coin_financials('bitcoin')

    def build_model(self, assetsUSD, assetsBTC):
        self.assets = []

        for idx, asset in enumerate(assetsUSD):
            self.assets.append(
                {
                    'name':                 asset['name'],
                    'symbol':               asset['symbol'],
                    'financials': {
                        'USD': {
                            'price':                                asset['current_price'],
                            'market_cap':                           asset['market_cap'],
                            'market_cap_rank':                      asset['market_cap_rank'],
                            'high_24h':                             asset['high_24h'],
                            'low_24h':                              asset['low_24h'],
                            'price_change_24h':                     asset['price_change_24h'],
                            'total_volume':                         asset['total_volume'],
                            'ath':                                  asset['ath'],
                            'ath_change_percentage':                asset['ath_change_percentage'],
                            'ath_date':                             asset['ath_date'],
                            'market_cap_change_24h':                asset['market_cap_change_24h'],
                            'circulating_supply':                   asset['circulating_supply'],
                            'total_supply':                         asset['total_supply'],
                            'market_cap_change_percentage_24h':     asset['market_cap_change_percentage_24h'],
                            'percent_change_24h':                   asset['price_change_percentage_24h'],       
                            'roi':                                  asset['roi'],       
                            
                            # 'percent_change_1h':                    asset['percent_change_1h'],
                            # 'market_change_24h':                    asset['market_change_24h'],
                            # 'volume_24h':                           asset['volume_24h'],
                            # 'percent_change_7d':                    asset['quote']['USD']['percent_change_7d'],   
                        },
                        'BTC': {
                            'price':                                assetsBTC[idx]['current_price'],
                            'market_cap':                           assetsBTC[idx]['market_cap'],
                            'market_cap_rank':                      assetsBTC[idx]['market_cap_rank'],
                            'high_24h':                             assetsBTC[idx]['high_24h'],
                            'low_24h':                              assetsBTC[idx]['low_24h'],
                            'price_change_24h':                     assetsBTC[idx]['price_change_24h'],
                            'total_volume':                         assetsBTC[idx]['total_volume'],
                            'ath':                                  assetsBTC[idx]['ath'],
                            'ath_change_percentage':                assetsBTC[idx]['ath_change_percentage'],
                            'ath_date':                             assetsBTC[idx]['ath_date'],
                            'market_cap_change_24h':                assetsBTC[idx]['market_cap_change_24h'],
                            'circulating_supply':                   assetsBTC[idx]['circulating_supply'],
                            'total_supply':                         assetsBTC[idx]['total_supply'],
                            'market_cap_change_percentage_24h':     assetsBTC[idx]['market_cap_change_percentage_24h'],
                            'percent_change_24h':                   assetsBTC[idx]['price_change_percentage_24h'],       
                            'roi':                                  assetsBTC[idx]['roi'],        
                        },
                        'created_date': dt.datetime.now()
                    },
                }
            )

    def does_coin_exist(self, token_name, token_symbol):
        self.coin = list(filter(lambda n: n.get('name').lower() == token_name.lower() and n.get('symbol').lower() == token_symbol.lower(), self.coins_list))

        if len(self.coin) == 0:
            self.coin = list(filter(lambda n: n.get('name').lower() == token_name.lower(), self.coins_list))
            if len(self.coin) > 0:
                self.helper.options['WARNING'](token_name, token_symbol, 2, 'coingecko')

        if len(self.coin) == 0:
            self.coin = list(filter(lambda n: n.get('symbol').lower() == token_symbol.lower(), self.coins_list))
            if len(self.coin) > 0:
                self.helper.options['WARNING'](token_name, token_symbol, 3, 'coingecko')


        if len(self.coin) > 0:
            self.coin = self.coin[0]
        elif not any(self.coin):
            self.helper.options['NOT_FOUND'](token_name, token_symbol, 'coingecko')
            return False


        return any(self.coin)

    def get_coin_financials(self):
        self.coin_info = self.req.get_data(
            cfg.settings['COINGECKO']['URLs']['FINANCIALS']['LINK'].format(self.coin['id']),
            params=cfg.settings['COINGECKO']['URLs']['FINANCIALS']['ARGS']['STANDARD'])

        return self.trim_info()


    # this gets all the financial information for each coin (inefficient)
    def compute_financials(self):
        coin_count = math.ceil(len(self.coins_list) / cfg.settings['COINGECKO']['COINS_MARKETS']['PARAMS']['STANDARD']['per_page']) 
        
        assetsUSD = []
        assetsBTC = []
        for i in range(coin_count):
            assetsUSD.extend(self.req.get_data(
                cfg.settings['COINGECKO']['URLs']['MARKETS']['LINK'], 
                params={
                    **cfg.settings['COINGECKO']['URLs']['MARKETS']['ARGS']['USD'],
                    **cfg.settings['COINGECKO']['URLs']['MARKETS']['ARGS']['STANDARD'] 
                },
                dynamic={ 'page': i+1 }
            ))
            assetsBTC.extend(self.req.get_data(
                cfg.settings['COINGECKO']['COINS_MARKETS']['URL'], 
                params={
                    **cfg.settings['COINGECKO']['URLs']['MARKETS']['ARGS']['BTC'],
                    **cfg.settings['COINGECKO']['URLs']['MARKETS']['ARGS']['STANDARD'] 
                },
                dynamic={ 'page': i+1 }
            ))

        self.build_model(assetsUSD, assetsBTC)

    # this gets a list of all coins and their IDs
    def get_coins_list(self):
        self.coins_list = self.req.get_data(cfg.settings['COINGECKO']['URLs']['COINLIST']['LINK'])

    def get_social_activity(self):
         self.details = {
            'coingecko': {
                'community': {
                    'sentiment': {
                        'sentiment_votes_up_percentage':            self.coin_info['sentiment_votes_up_percentage'],
                        'sentiment_votes_down_percentage':          self.coin_info['sentiment_votes_down_percentage']
                    },      
                    'roi':                                          self.coin_info['market_data']['roi'], 
                    'rank':                                         self.coin_info['market_data']['market_cap_rank'],
                    'counts': {     
                        'facebook_count':                           self.coin_info['community_data']['facebook_likes'],
                        'twitter_count':                            self.coin_info['community_data']['twitter_followers'],
                        'telegram_count':                           self.coin_info['community_data']['telegram_channel_user_count'],
                        'public_interest_stats': {
                            'alexa_rank':                           self.coin_info['public_interest_stats']['alexa_rank'],
                            'bing_matches':                         self.coin_info['public_interest_stats']['bing_matches'],
                        },  
                        'reddit': { 
                            'average_posts_48h':                    self.coin_info['community_data']['reddit_average_posts_48h'],
                            'average_comments_48h':                 self.coin_info['community_data']['reddit_average_comments_48h'],
                            'subscribers':                          self.coin_info['community_data']['reddit_subscribers'],
                            'accounts_active_48h':                  self.coin_info['community_data']['reddit_accounts_active_48h'],
                        }       
                    },      
                    'rankings': {       
                        'coingecko_rank':                           self.coin_info['coingecko_score'],
                        'developer_score':                          self.coin_info['developer_score'],
                        'community_score':                          self.coin_info['community_score'],
                        'liquidity_score':                          self.coin_info['liquidity_score'],
                        'public_interest_score':                    self.coin_info['public_interest_score'],
                    }       
                },      
                'technical': {      
                    'hashing_algorithm':                            self.coin_info['hashing_algorithm'],
                    'genesis_date':                                 self.coin_info['genesis_date'],
                    'country_origin':                               self.coin_info['country_origin'],
                    'block_time_in_minutes':                        self.coin_info['block_time_in_minutes'],
                    'developer_data': {         
                        'forks':                                    self.coin_info['developer_data']['forks'],
                        'stars':                                    self.coin_info['developer_data']['stars'],
                        'subscribers':                              self.coin_info['developer_data']['subscribers'],
                        'total_issues':                             self.coin_info['developer_data']['total_issues'],
                        'closed_issues':                            self.coin_info['developer_data']['closed_issues'],
                        'pull_requests_merged':                     self.coin_info['developer_data']['pull_requests_merged'],
                        'pull_request_contributors':                self.coin_info['developer_data']['pull_request_contributors'],
                        'code_additions_deletions_4_weeks': {   
                            'additions':                            self.coin_info['developer_data']['code_additions_deletions_4_weeks']['additions'],
                            'deletions':                            self.coin_info['developer_data']['code_additions_deletions_4_weeks']['deletions'],
                        },  
                        'commit_count_4_weeks':                     self.coin_info['developer_data']['commit_count_4_weeks'],
                        'last_4_weeks_commits':                     self.coin_info['developer_data']['last_4_weeks_commit_activity_series'],
                    }   
                },
                'financials': {
                }
            }
        }


    def trim_info(self):
        currencies = ['btc', 'usd', 'eur', 'gbp', 'jpy', 'cad', 'sgd', 'nok', 'cny', 'aud', 'chf', 'nzd', 'inr']

        currency_financials = {}

        for currency in currencies:
            currency_formatted = currency.upper()            
            currency_financials[currency_formatted] = {}
            currency_financials[currency_formatted]['high_24h'] = self.coin_info['market_data']['high_24h'][currency]
            currency_financials[currency_formatted]['low_24h'] = self.coin_info['market_data']['low_24h'][currency]
            
            currency_financials[currency_formatted]['ath'] = {}
            currency_financials[currency_formatted]['ath']['price'] = self.coin_info['market_data']['ath'][currency]
            currency_financials[currency_formatted]['ath']['ath_change_percentage'] = self.coin_info['market_data']['ath_change_percentage'][currency]
            currency_financials[currency_formatted]['ath']['ath_date'] = self.coin_info['market_data']['ath_date'][currency]
            
            currency_financials[currency_formatted]['atl'] = {}
            currency_financials[currency_formatted]['atl']['price'] = self.coin_info['market_data']['atl'][currency]
            currency_financials[currency_formatted]['atl']['ath_change_percentage'] = self.coin_info['market_data']['atl_change_percentage'][currency]
            currency_financials[currency_formatted]['atl']['ath_date'] =  self.coin_info['market_data']['atl_date'][currency]
            
            currency_financials[currency_formatted]['price'] = {}
            currency_financials[currency_formatted]['price']['current_price'] = self.coin_info['market_data']['current_price'][currency]
            currency_financials[currency_formatted]['price']['change_24h'] =  self.coin_info['market_data']['price_change_24h_in_currency'][currency]
            
            currency_financials[currency_formatted]['price']['percent_change'] = {}
            currency_financials[currency_formatted]['price']['percent_change']['24h'] =  self.coin_info['market_data']['price_change_percentage_24h_in_currency'][currency]
            currency_financials[currency_formatted]['price']['percent_change']['7d'] =  self.coin_info['market_data']['price_change_percentage_7d_in_currency'][currency]
            
            currency_financials[currency_formatted]['valuation'] = {}
            currency_financials[currency_formatted]['valuation']['market_cap_value'] = self.coin_info['market_data']['market_cap'][currency]
            currency_financials[currency_formatted]['valuation']['market_cap_change_24h'] = self.coin_info['market_data']['market_cap_change_24h_in_currency'][currency]
            currency_financials[currency_formatted]['valuation']['market_cap_percent_change_24h'] = self.coin_info['market_data']['market_cap_change_percentage_24h_in_currency'][currency]
            currency_financials[currency_formatted]['valuation']['total_volume'] = self.coin_info['market_data']['total_volume'][currency]

            if 'price_change_percentage_1y_in_currency' in self.coin_info and bool(self.coin_info['price_change_percentage_1y_in_currency']):
                currency_financials[currency_formatted]['price']['percent_change']['1y'] = self.coin_info['market_data']['price_change_percentage_1y_in_currency'][currency]
                
            if 'price_change_percentage_200d_in_currency' in self.coin_info and bool(self.coin_info['price_change_percentage_1y_in_currency']):
                currency_financials[currency_formatted]['price']['percent_change']['200d'] = self.coin_info['market_data']['price_change_percentage_200d_in_currency'][currency]

            if 'price_change_percentage_14d_in_currency' in self.coin_info and bool(self.coin_info['price_change_percentage_14d_in_currency']):
                currency_financials[currency_formatted]['price']['percent_change']['14d'] =  self.coin_info['market_data']['price_change_percentage_14d_in_currency'][currency]
            
            if 'price_change_percentage_30d_in_currency' in self.coin_info and bool(self.coin_info['price_change_percentage_30d_in_currency']):
                currency_financials[currency_formatted]['price']['percent_change']['30d'] =  self.coin_info['market_data']['price_change_percentage_30d_in_currency'][currency]

            if 'price_change_percentage_60d_in_currency' in self.coin_info and bool(self.coin_info['price_change_percentage_60d_in_currency']):
                currency_financials[currency_formatted]['price']['percent_change']['60d'] =  self.coin_info['market_data']['price_change_percentage_60d_in_currency'][currency]

            if 'price_change_percentage_1h_in_currency' in self.coin_info and bool(self.coin_info['price_change_percentage_1h_in_currency']):
                currency_financials[currency_formatted]['price']['percent_change']['1h'] = self.coin_info['market_data']['price_change_percentage_1h_in_currency'][currency]


        currency_financials['created_date'] =  dt.datetime.now()

        return currency_financials
        # self.details['coingecko']['financials'][currency.upper()] = currency_financials

    def get_asset(self, token):
        pass
        # if list(filter(lambda n: n.get('symbol').lower() == token.lower(), self.assets)):
        #     return self.trim_financials(token)

    def get_financials(self, token):
        pass
        # asset_financials = self.get_asset(token)
        # return asset_financials if asset_financials else None
