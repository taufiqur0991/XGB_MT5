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
        "use_fixed_lot": False,
        "fixed_lot_size": 0.02,
    },
    "GBPUSD": {
        "model": "model/GBPUSD.pkl",
        "sl_pips": 10,
        "tp_pips": 15,
        "max_spread_sl_pct": 0.3,
        "use_fixed_lot": True,
        "fixed_lot_size": 0.03,
    },
    "XAUUSD": {
        "model": "model/XAUUSD.pkl",
        "sl_pips": 100,
        "tp_pips": 150,
        "max_spread_sl_pct": 0.25,
        "use_fixed_lot": True,
        "fixed_lot_size": 0.01,
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
