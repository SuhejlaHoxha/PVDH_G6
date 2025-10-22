import json
import csv
from pathlib import Path


def flatten(obj, parent_key='', sep='.'):
    items = []
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            items.extend(flatten(v, f"{parent_key}[{i}]", sep=sep).items())
    elif isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, obj))
    return dict(items)


def json_to_csv(json_path: str, csv_path: str):
    rows = []
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

        try:
            data = json.loads(content)  
            if isinstance(data, dict):
                data = [data]
        except:
            data = [json.loads(line) for line in content.splitlines() if line.strip()]

    for obj in data:
        rows.append(flatten(obj))

    all_headers = sorted({key for r in rows for key in r.keys()})

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done: CSV saved -> {csv_path}")


if __name__ == "__main__":
    json_to_csv("gcpRawAuditLogs.json", "gcpRawAuditLogs.csv")
