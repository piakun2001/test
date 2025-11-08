import csv
import random
from pathlib import Path
import argparse

# CSV path: same name as this script but with .csv extension
csv_path = Path(__file__).with_suffix('.csv')

def load_rows(path):
    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # convert numeric fields if possible
            try:
                r["id"] = int(r["id"])
            except Exception:
                pass
            try:
                r["value"] = float(r["value"])
            except Exception:
                pass
            rows.append(r)
    return rows

TEMPLATES = [
    "{name} (id {id}) has a value of {value:.1f}.",
    "Record #{id}: {name} — value {value:.1f}.",
    "{name}'s score is {value:.1f} (id {id}).",
    "{name} (#{id}) — measured: {value:.1f}."
]

def describe_value(value):
    try:
        v = float(value)
    except Exception:
        return ""
    if v >= 80:
        return "very high"
    if v >= 50:
        return "high"
    if v >= 20:
        return "moderate"
    return "low"

def generate(rows, n=5):
    out = []
    for _ in range(n):
        row = random.choice(rows)
        tpl = random.choice(TEMPLATES)
        desc = describe_value(row.get("value", 0))
        text = tpl.format(name=row.get("name", "Unknown"),
                          id=row.get("id", "?"),
                          value=row.get("value", 0))
        # optional adjective append
        out.append(f"{text} ({desc})" if desc else text)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple generative sentences from CSV")
    parser.add_argument("--n", type=int, default=5, help="number of sentences to generate")
    args = parser.parse_args()

    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
    else:
        rows = load_rows(csv_path)
        for line in generate(rows, args.n):
            print(line)
