from detect_dtypes import detect_dtypes
from data_quality_check import data_quality_check

CSV_INPUT = "dataset/gcpRawAuditLogs.csv"

def main():
    dtypes = detect_dtypes(CSV_INPUT)

    print("\n--- DATA TYPES DETECTED ---\n")
    for col, tp in dtypes.items():
        print(f"{col} → {tp}")

    print("\n--- DATA QUALITY CHECK ---\n")
    data_quality_check(CSV_INPUT)

if __name__ == "__main__":
    main()
