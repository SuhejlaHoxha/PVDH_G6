import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_eda(input_csv: str):
    df = pd.read_csv(input_csv, low_memory=False)

    # Automatically detect numeric columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns

    print("\n--- EXPLORATORY DATA ANALYSIS (EDA) ---")
    print(f"Numeric columns detected: {list(num_cols)}")

    if len(num_cols) == 0:
        print("❌ No numeric columns found. EDA skipped.")
        return {}

    print("\n--- SUMMARY STATISTICS ---")
    print(df[num_cols].describe())

    # If only one numeric column, skip correlation heatmap
    if len(num_cols) < 2:
        print("\n Only one numeric column found. Correlation matrix requires at least 2 columns.")
        corr = df[num_cols].corr()
        print("\nCorrelation matrix:")
        print(corr)
        return {
            "numeric_columns_analyzed": len(num_cols),
            "heatmap_saved": None
        }

    # Correlation matrix
    print("\n--- CORRELATION MATRIX ---")
    corr = df[num_cols].corr()
    print(corr)

    # Save heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=True)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    path = "dataset/eda_correlation_heatmap.png"
    plt.savefig(path)
    plt.close()

    return {
        "numeric_columns_analyzed": len(num_cols),
        "heatmap_saved": path
    }
