def resolve_symbol(raw: str, symbols, fallbacks=("USDT", "USDC", "USD")):
    r = raw.upper().replace("-", "").replace("_", "")
    if r in symbols:
        return r
    if "/" in r and r.replace("/", "") in symbols:
        return r.replace("/", "")
    base = r.split("/")[0] if "/" in r else r
    for q in fallbacks:
        cand = f"{base}{q}"
        if cand in symbols:
            return cand
    raise ValueError(raw)
