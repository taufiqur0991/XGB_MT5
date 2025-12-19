import MetaTrader5 as mt5

# ======================
# TRADING CONFIG
# ======================
SYMBOLS = {
    "EURUSD": {
        "model": "model/EURUSD.pkl",
        "sl_pips": 10,
        "tp_pips": 15,
        "max_spread_sl_pct": 0.3,  # 30% SL
    },
    "GBPUSD": {
        "model": "model/GBPUSD.pkl",
        "sl_pips": 12,
        "tp_pips": 18,
        "max_spread_sl_pct": 0.3,
    },
    "XAUUSD": {
        "model": "model/XAUUSD.pkl",
        "sl_pips": 150,
        "tp_pips": 300,
        "max_spread_sl_pct": 0.25,
    }
}

# ======================
# TRAILING CONFIG
# ======================
TRAILING = {
    "enable": True,

    # mulai trailing jika profit >= ini (pips)
    "start_pips": 8,

    # jarak SL dari harga (pips)
    "distance_pips": 5,

    # trailing profit (lock)
    "lock_steps": [
        (10, 3),   # profit >=10 → SL +3
        (20, 10),  # profit >=20 → SL +10
        (30, 20),
    ]
}


TIMEFRAME = mt5.TIMEFRAME_M5
LOT_RISK = 0.01
MAGIC = 202501
