import MetaTrader5 as mt5
import joblib
import pandas as pd
from features import build_features
from risk import spread_ok, calc_lot, PIP_MAP
from execution import open_trade

def process_symbol(symbol, cfg):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)
    df = pd.DataFrame(rates)

    df.rename(columns={
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close"
    }, inplace=True)

    df_feat = build_features(df)
    X = df_feat.iloc[-1:][['return','ema9','ema21','rsi','body','range']]

    model = joblib.load(cfg['model'])
    proba = model.predict_proba(X)[0]

    buy_p, sell_p = proba[1], proba[0]

    if max(buy_p, sell_p) < 0.6:
        return

    direction = "BUY" if buy_p > sell_p else "SELL"

    if not spread_ok(symbol, cfg['sl_pips'], cfg['max_spread_sl_pct']):
        print(f"⛔ Spread terlalu besar {symbol}")
        return

    acc = mt5.account_info()
    lot = calc_lot(acc.balance, cfg['sl_pips'])

    tick = mt5.symbol_info_tick(symbol)
    pip = PIP_MAP[symbol]

    if direction == "BUY":
        sl = tick.ask - cfg['sl_pips'] / pip
        tp = tick.ask + cfg['tp_pips'] / pip
    else:
        sl = tick.bid + cfg['sl_pips'] / pip
        tp = tick.bid - cfg['tp_pips'] / pip

    open_trade(symbol, direction, lot, sl, tp, magic=202501)
