from data.utils import resolve_symbol
def test_direct():  assert resolve_symbol("btcUSDT", ["BTCUSDT"]) == "BTCUSDT"
def test_slash():   assert resolve_symbol("btc/usdt", ["BTCUSDT"]) == "BTCUSDT"
def test_fallback():assert resolve_symbol("btc", ["BTCUSD"]) == "BTCUSD"
