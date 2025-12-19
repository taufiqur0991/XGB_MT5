import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['return'] = df['close'].pct_change()
    df['ema9'] = EMAIndicator(df['close'], 9).ema_indicator()
    df['ema21'] = EMAIndicator(df['close'], 21).ema_indicator()
    df['rsi'] = RSIIndicator(df['close'], 14).rsi()
    df['body'] = df['close'] - df['open']
    df['range'] = df['high'] - df['low']

    return df.dropna()
