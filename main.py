from detect_dtypes import detect_dtypes
from data_quality_check import data_quality_check
from aggregate_logs import aggregate_by_cluster, aggregate_by_decision, aggregate_by_user, aggregate_by_status_code, aggregate_by_location
from sample_logs import sample_logs

CSV_INPUT = "dataset/gcpRawAuditLogs.csv"

def main():
    dtypes = detect_dtypes(CSV_INPUT)

    print("\n--- DATA TYPES DETECTED ---\n")
    for col, tp in dtypes.items():
        print(f"{col} → {tp}")

    print("\n--- DATA QUALITY CHECK ---\n")
    data_quality_check(CSV_INPUT)

    print("\n--- AGGREGATION STEP ---\n")
    aggregate_by_decision(CSV_INPUT)
    aggregate_by_cluster(CSV_INPUT)
    aggregate_by_user(CSV_INPUT)
    aggregate_by_status_code(CSV_INPUT)
    aggregate_by_location(CSV_INPUT)

    print("\n--- SAMPLING STEP ---\n")
    sample_logs(CSV_INPUT)

if __name__ == "__main__":
    main()
