import pandas as pd

# 1 Agregim sipas vendimit (allow / forbid)
def aggregate_by_decision(csv_file):
    df = pd.read_csv(csv_file)
    decision_counts = df['labels.authorization.k8s.io/decision'].value_counts()

    print("\n--- NUMRI I LOGJEVE SIPAS VENDIMIT (ALLOW / FORBID) ---\n")
    print(decision_counts)
    return decision_counts


# 2️ Agregim sipas emrit të clusterit
def aggregate_by_cluster(csv_file):
    df = pd.read_csv(csv_file)
    cluster_counts = df['resource.labels.cluster_name'].value_counts()

    print("\n--- NUMRI I LOGJEVE SIPAS CLUSTERËVE ---\n")
    print(cluster_counts)
    return cluster_counts


# 3️ Agregim sipas përdoruesit (email)
def aggregate_by_user(csv_file):
    df = pd.read_csv(csv_file)
    user_counts = df['protoPayload.authenticationInfo.principalEmail'].value_counts()

    print("\n--- NUMRI I LOGJEVE SIPAS PËRDORUESIT ---\n")
    print(user_counts.head(10))  # vetëm 10 më aktivët
    return user_counts


# 4️ Agregim sipas statusit të përgjigjes (status code)
def aggregate_by_status_code(csv_file):
    df = pd.read_csv(csv_file)
    status_counts = df['protoPayload.status.code'].value_counts()

    print("\n--- NUMRI I LOGJEVE SIPAS KODIT TË STATUSIT ---\n")
    print(status_counts)
    return status_counts


# 5️ Agregim sipas lokacionit (regionit)
def aggregate_by_location(csv_file):
    df = pd.read_csv(csv_file)
    location_counts = df['resource.labels.location'].value_counts()

    print("\n--- NUMRI I LOGJEVE SIPAS LOKACIONIT ---\n")
    print(location_counts)
    return location_counts
