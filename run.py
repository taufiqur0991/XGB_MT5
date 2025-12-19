import MetaTrader5 as mt5
import time
from config import *
from trader import process_symbol
from trailing import apply_trailing

mt5.initialize()

print("🚀 MT5 Trader + Trailing Started")

while True:
    for symbol, cfg in SYMBOLS.items():
        process_symbol(symbol, cfg)

        if TRAILING['enable']:
            apply_trailing(symbol, TRAILING)

    time.sleep(10)
