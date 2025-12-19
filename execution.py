import MetaTrader5 as mt5

# =========================
# CHECK POSITION (PER SYMBOL + MAGIC)
# =========================
def has_open_position(symbol, magic):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return False

    for p in positions:
        if p.magic == magic:
            return True
    return False
# =========================
# OPEN TRADE (SAFE)
# =========================
def open_trade(symbol, direction, lot, sl, tp, magic):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print("❌ Symbol not found")
        return None

    if not symbol_info.visible:
        mt5.symbol_select(symbol, True)

    # ===== GUARD POSITION =====
    if has_open_position(symbol, magic):
        print(f"⏸ {symbol} | Position still open")
        return None

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print("❌ No tick data")
        return None

    # ===== PRICE =====

    if direction == "BUY":
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY
    else:
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": magic,
        "comment": "XGB_PYTHON",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    # ===== RESULT CHECK =====
    if result is None:
        print("❌ order_send failed")
        return None

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Order failed: {result.retcode}")
        return None

    print(f"✅ {direction} {symbol} opened | ticket={result.order}")
    return result
