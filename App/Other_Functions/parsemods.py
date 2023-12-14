def parse(mods):
    mods = [mod.lower() for mod in mods]
    total = 0
    if "ez" in mods:
        total+=2
    if "hr" in mods:
        total+=16
    if "dt" in mods:
        total+=64
    if "ht" in mods:
        total+=256
    if "nc" in mods:
        total+=512
    return total