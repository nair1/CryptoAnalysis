from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import xlsxwriter

class Coin:
    def __init__(self, name, rank, m_cap, id):
        self.name = name
        self.rank = rank
        self.m_cap = m_cap
        self.id = id 

def get_coin_list():
    key = "ea151f74-c4a6-4408-96d1-1ee6981c3c31"
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    final_list = []

    parameters = {
    'start':'1',
    'limit':'300',
    'convert':'USD'
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        coin_list = data.get('data')

        print(len(coin_list))
        
        for coin in coin_list:
            id = coin.get('id')
            name = coin.get('symbol')
            cmc_rank = str(coin.get('cmc_rank'))
            quote = coin.get('quote')
            usd_quote = quote.get('USD')

            market_cap = str(round(usd_quote.get('market_cap')))

            if ("stablecoin" not in coin.get('tags')):
                #print('(' + cmc_rank + ') ' + name + ": " + market_cap)
                coin_to_add = Coin(name, cmc_rank, market_cap, id)
                final_list.append(coin_to_add)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    return final_list

def create_xlsx(coin_list):
    workbook = xlsxwriter.Workbook('crypto_data.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Rank')
    worksheet.write(0, 1, 'Name')
    worksheet.write(0, 2, 'Market Cap')
    worksheet.write(0, 3, 'Subreddit')
    worksheet.write(0, 4, 'Number of Users')
    worksheet.write(0, 5, 'Per User Value')

    row = 1

    for coin in coin_list:
        worksheet.write(row, 0, coin.rank)
        worksheet.write(row, 1, coin.name)
        worksheet.write(row, 2, coin.m_cap)

        url = 'https://s2.coinmarketcap.com/static/img/coins/64x64/' + str(coin.id) + '.png'

        worksheet.write(row, 3, url)

        row += 1

    workbook.close()  

coin_list = get_coin_list()
create_xlsx(coin_list)