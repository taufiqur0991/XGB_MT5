import MetaTrader5 as mt5
from risk import PIP_MAP

def apply_trailing(symbol, trailing_cfg):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return

    tick = mt5.symbol_info_tick(symbol)
    pip = PIP_MAP[symbol]

    for pos in positions:
        if pos.magic != 202501:
            continue

        # =====================
        # HITUNG PROFIT PIPS
        # =====================
        if pos.type == mt5.ORDER_TYPE_BUY:
            profit_pips = (tick.bid - pos.price_open) * pip
        else:
            profit_pips = (pos.price_open - tick.ask) * pip

        if profit_pips < trailing_cfg['start_pips']:
            continue

        new_sl = None

        # =====================
        # TRAILING PROFIT LOCK
        # =====================
        for lvl, lock in trailing_cfg['lock_steps']:
            if profit_pips >= lvl:
                if pos.type == mt5.ORDER_TYPE_BUY:
                    new_sl = pos.price_open + lock / pip
                else:
                    new_sl = pos.price_open - lock / pip

        # =====================
        # TRAILING DISTANCE
        # =====================
        if pos.type == mt5.ORDER_TYPE_BUY:
            dist_sl = tick.bid - trailing_cfg['distance_pips'] / pip
            new_sl = max(new_sl or dist_sl, dist_sl)

            if pos.sl == 0 or new_sl > pos.sl:
                modify_sl_tp(pos, new_sl, pos.tp)

        else:
            dist_sl = tick.ask + trailing_cfg['distance_pips'] / pip
            new_sl = min(new_sl or dist_sl, dist_sl)

            if pos.sl == 0 or new_sl < pos.sl:
                modify_sl_tp(pos, new_sl, pos.tp)


def modify_sl_tp(pos, sl, tp):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": pos.ticket,
        "sl": sl,
        "tp": tp
    }
    mt5.order_send(request)
