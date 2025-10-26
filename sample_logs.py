import pandas as pd

def sample_logs(csv_path):
    """
    Merr 30% të të dhënave rastësore dhe i ruan në 'sample_30_percent.csv'.
    """
    df = pd.read_csv(csv_path)

    # Mostrim 30% i të dhënave
    sample_df = df.sample(frac=0.3, random_state=42)

    print("Mostra 30% e të dhënave:")
    print(sample_df.head())
