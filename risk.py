import MetaTrader5 as mt5

PIP_MAP = {
    "EURUSD": 10000,
    "GBPUSD": 10000,
    "XAUUSD": 10
}

def spread_ok(symbol, sl_pips, max_pct):
    tick = mt5.symbol_info_tick(symbol)
    spread_pips = abs(tick.ask - tick.bid) * PIP_MAP[symbol]
    return spread_pips <= sl_pips * max_pct

def calc_lot(balance, sl_pips, pip_value=10, risk=0.01):
    risk_usd = balance * risk
    return round(risk_usd / (sl_pips * pip_value), 2)
