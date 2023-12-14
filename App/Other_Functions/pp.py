from math import log10

def calcpp(sr,ar,combo,mods):
    final = []
    if "hr" in mods:
        ar *= 1.4
        ar = 10 if ar>10 else ar
    if "ez" in mods:
        ar /= 2
    if "ht" in mods:
        arms = (1600 + ((5-ar) * 160)) if ar < 6 else (1600 - ((ar-5) * 200))
        ar = (5 + ((1200-arms) / 150)) if arms <= 1200 else (5 - ((1200-arms) / 120))
    if "dt" in mods or "nc" in mods:
        arms = (800 + ((5-ar) * 80)) if ar < 6 else (800 - ((ar-5) * 100))
        ar = (5 + ((1200-arms) / 150)) if arms <= 1200 else (5 - ((1200-arms) / 120))
    ar = 11 if ar>11 else ar
    pp = (((5*max(1.0,sr/0.0049))-4)**2)/100000
    if "fl" not in mods:
        pp *= 0.95 + 0.3 * min(1.0,combo/2500.0) + ((log10(combo/2500.0)*0.475) if combo>2500 else 0.0)
    else:
        pp *= (0.95 + 0.3 * min(1.0,combo/2500.0) + ((log10(combo/2500.0)*0.475) if combo>2500 else 0.0)) * 1.35
    arbonus = 1
    if ar<8:
        arbonus += 0.025 * (8.0 - ar)
    if ar>9:
        arbonus += 0.1 * (ar - 9.0)
    if ar>10:
        arbonus += 0.1 * (ar - 10.0)
    pp *= arbonus
    if ar>10:
        hiddenbonus = 1.01 + 0.04 * (11-min(11,ar))
    else:
        hiddenbonus = 1.05 + 0.075 * (10-ar)
    if "hd" in mods:
        pp *= hiddenbonus
    final.append(round(pp*((100/100)**5.5)))
    final.append(round(pp*((99/100)**5.5)))
    final.append(round(pp*((98/100)**5.5)))
    return final