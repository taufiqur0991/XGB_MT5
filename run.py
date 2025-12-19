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
        # Ambil config trailing dari cfg simbol tersebut
        symbol_trailing_cfg = cfg.get('trailing')
        if symbol_trailing_cfg and cfg.get('use_trailing', False):
            apply_trailing(symbol, symbol_trailing_cfg)

    time.sleep(10)
