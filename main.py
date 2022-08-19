from re import template
import sqlite3, config
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI() 
templates = Jinja2Templates(directory="templates")
 
@app.get('/')
def index(request: Request):
    connection = sqlite3.connect(config.DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
    """)
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows}) 

@app.get('/stock/{symbol}')
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM strategy
    """)

    strategies = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM stock WHERE symbol = ? 
    """, (symbol, ))
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date
    """, (row["id"], ))
    
    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock" : row, "prices" : prices, "strategies" : strategies}) 


@app.post('/apply_strategy')
def apply_strategy(strategy_id:int = Form(...),stock_id:int = Form(...)):
    connection = sqlite3.connect(config.DB_FILE_PATH)
    cursor = connection.cursor()
    print(strategy_id)

    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?,?)
    """, (stock_id, strategy_id, ))

    connection.commit()

    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)

@app.get('/strategy/{strategy_id}')
def index(request: Request, strategy_id:int):
    connection = sqlite3.connect(config.DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name FROM strategy
        WHERE id = ?
    """, (strategy_id, ))

    strategy = cursor.fetchone()

    cursor.execute("""
        SELECT symbol, name FROM stock
        JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """, (strategy_id, ))
    stocks = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request":request, "stocks":stocks, "strategy" : strategy})