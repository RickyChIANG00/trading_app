import sqlite3, config
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(config.DB_FILE_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

api = tradeapi.REST(config.API_KEY_ID,config.API_SECRET_KEY,base_url = config.API_URL)
assets = api.list_assets()

cursor.execute("""SELECT  symbol, name FROM stock""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]



for asset in assets:
    try:
        if asset.symbol not in symbols and asset.status == 'active' and asset.tradable == True and asset.exchange != 'FTXU':
            print(f"Added a new stock {asset.symbol}: {asset.name}")
            cursor.execute('INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)', (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()