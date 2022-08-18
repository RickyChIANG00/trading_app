import sqlite3, config
import alpaca_trade_api as tradeapi
 
connection = sqlite3.connect(config.DB_FILE_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")
rows = cursor.fetchall()

symbols=[]
stock_dict = {}

for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY_ID,config.API_SECRET_KEY,base_url = config.API_URL)

chunk_size = 200
for i in range (0,len(symbols),chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    print("processing symbol no.{} to {}". format(i, i+chunk_size))
    barsets = api.get_bars(symbol_chunk, '1Day', '2022-01-01T10:00:00-05:00')
    for bar in barsets:
        stock_id = stock_dict[bar.S]
        cursor.execute("""
            INSERT INTO stock_price(stock_id, date, open, high, low, close, volume)
            VALUES (?,?,?,?,?,?,?)
        """, (stock_id, bar.t.date(),bar.o,bar.h,bar.l,bar.c,bar.v))

connection.commit()
