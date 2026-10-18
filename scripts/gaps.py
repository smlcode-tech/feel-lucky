"""Writes data/eksikler.csv: every expected draw that is missing, or present with an empty Joker/SüperStar.

Usage: python3 -I scripts/gaps.py [candidates_file ...]
Candidate files use the pipe format of the collection agents; their numbers are noted as unconfirmed.
"""
import csv
import datetime as D
import json
import sys

draws = {x["date"]: x for x in json.load(open("data/results.json"))["draws"]}

candidates = {}
for path in sys.argv[1:]:
    for raw in open(path):
        p = [s.strip() for s in raw.strip().split("|")]
        if len(p) >= 8 and p[0][:4].isdigit():
            candidates[p[0]] = p

# A missing first draw of the period only shows up among the candidates.
first = D.date.fromisoformat(min([*draws, *candidates]))
last = D.date.fromisoformat(max(draws))


def ordinal(d):
    s = D.date(d.year, 1, 1)
    return sum(1 for i in range((d - s).days + 1) if (s + D.timedelta(i)).weekday() in (0, 2, 5))


rows = []
d = first
while d <= last:
    if d.weekday() in (0, 2, 5):
        key = d.isoformat()
        x = draws.get(key)
        if x is None:
            c = candidates.get(key)
            known = c is not None and c[2] not in ("?", "", "UNRESOLVED") and "?" not in c[2]
            reason = "tek kaynakta bulundu, doğrulanmadı" if known else "numaralar hiçbir kaynakta bulunamadı"
            if c is not None and c[7]:
                reason += f" ({c[7]})"
            rows.append([key, ordinal(d), "tüm çekiliş", reason,
                         c[2] if known else "", c[3] if known else "", c[4] if known else ""])
        else:
            missing = [name for name, v in (("Joker", x["joker"]), ("SüperStar", x["superstar"])) if v is None]
            if missing:
                rows.append([key, x["drawNo"], " ve ".join(missing), "kaynaklar çelişiyor veya etiketsiz", "", "", ""])
    d += D.timedelta(1)

with open("data/eksikler.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["tarih", "cekilis_no", "eksik", "neden", "aday_numaralar", "aday_joker", "aday_superstar"])
    w.writerows(rows)
print(len(rows), "satır")
