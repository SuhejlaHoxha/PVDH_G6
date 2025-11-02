from detect_dtypes import detect_dtypes
from data_quality_check import data_quality_check
from aggregate_logs import aggregate_by_cluster, aggregate_by_decision, aggregate_by_user, aggregate_by_status_code, aggregate_by_location
from sample_logs import sample_logs
from clean_null_values import clean_dataset
from feature_engineering import run_feature_engineering
from encode_scale_and_pca import run_encode_scale_pca
from discretize_binarize import run_discretize_binarize
from transform_normalize import run_transformations

CSV_INPUT = "dataset/gcpRawAuditLogs.csv"
CSV_CLEAN = "dataset/gcpRawAuditLogs_cleaned.csv"

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

    print("\n--- CLEANING STEP ---\n")
    clean_dataset(CSV_INPUT, "dataset/gcpRawAuditLogs_cleaned.csv")

    print("\n--- FEATURE ENGINEERING ---\n")
    fe_out = "dataset/processed/features_engineered_basic.csv"
    fe_info = run_feature_engineering(CSV_CLEAN, fe_out)
    print("Feature engineering summary:", fe_info)

    print("\n--- ENCODE + SCALE + PCA ---\n")
    enc_out = "dataset/processed/features_encoded_scaled.csv"
    pca_out = "dataset/processed/features_pca10.csv"
    enc_info = run_encode_scale_pca(fe_out, enc_out, pca_out, top_k=20, n_components=10)
    print("Encoding/PCA summary:", enc_info)


if __name__ == "__main__":
    main()
