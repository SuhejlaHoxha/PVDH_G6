# PVDH_G6 - Cloud Audit Logs

**University of Prishtina – Faculty of Electrical and Computer Engineering (FIEK)**  
**Program:** Computer and Software Engineering – Master  
**Course:** Data Preparation and Visualization  
**Professor:** Prof. Dr. Mërgim Hoti  

---

## Contributors
- Dredhza Braina  
- Art Ukshini  
- Suhejla Hoxha  

---

## Project Overview

This project focuses on **analyzing and preparing Google Cloud Audit Logs** for data quality inspection, preprocessing, and feature extraction.  
The main objective is to create a **clean, structured, and analysis-ready dataset** that supports auditing insights, authorization tracking, and anomaly detection.

The dataset represents Kubernetes (K8s) audit logs, containing event metadata about API requests, authorization decisions, user actions, and resource operations across multiple clusters and regions.

---

## Project Goals

- Build a **complete data preprocessing pipeline** using Python.  
- Apply **feature engineering** to enrich event-level logs with analytical attributes.  
- Handle **missing, duplicate, or inconsistent data** in audit records.  
- Aggregate and summarize logs by cluster, location, user, and authorization type.  
- Implement **modular and reusable Python scripts** for every pipeline stage.  
- Ensure **efficiency and scalability** for large-scale log datasets.  
- Prepare datasets for further **security analytics and visualization**.

---

## Technologies Used

| Tool / Library | Purpose |
|----------------|----------|
| **Python 3.11** | Main programming language |
| **pandas**, **numpy** | Data cleaning and transformation |
| **scikit-learn** | Feature preprocessing, normalization, PCA |
| **datetime**, **re**, **os**, **pathlib** | Parsing, regex filtering, and file management |

---

## Dataset Description

The dataset used for this project is derived from **Google Cloud Audit Logs**, focusing on Kubernetes activity.  
Each log entry describes an authorization event within a Kubernetes cluster.

### Sample Attributes

| Attribute | Description | Example |
|------------|--------------|----------|
| `insertId` | Unique event identifier | `consolidated_event_1_761316` |
| `labels.authorization.k8s.io/decision` | Authorization result | `forbid` |
| `labels.authorization.k8s.io/reason` | Reason for the decision | `RBAC: access denied` |
| `logName` | Log source path | `projects/project123/logs/cloudaudit.googleapis.com%2Factivity` |
| `protoPayload.authenticationInfo.principalEmail` | User performing the action | `admin@company.com` |
| `protoPayload.authorizationInfo[0].permission` | Accessed permission | `io.k8s.patch` |
| `protoPayload.methodName` | Method/API called | `io.k8s.patch` |
| `protoPayload.requestMetadata.callerIp` | IP of the caller | `217.71.49.51` |
| `protoPayload.requestMetadata.callerSuppliedUserAgent` | Client information | `kubectl/v1.26.0 (darwin/amd64)` |
| `resource.labels.cluster_name` | Kubernetes cluster name | `prod-cluster` |
| `resource.labels.location` | Cluster region | `europe-west1` |
| `resource.labels.project_id` | Cloud project identifier | `project123` |
| `timestamp` | Event timestamp | `2024-11-03T16:38:07Z` |

---

## Main Pipeline: Cloud Audit Log Preprocessing

The `main.py` script orchestrates the **complete preprocessing and transformation workflow**.  
It integrates multiple modules to clean, transform, and enrich audit log data for downstream analytics.

### Workflow Steps

#### 1. **Data Type Conversion**
- Converts raw Google Audit Log fields to appropriate types:
  - `insertId` → `string`
  - `labels.authorization.k8s.io/decision` → `string`
  - `labels.authorization.k8s.io/reason` → `string`
  - `logName` → `string`
  - `operation.first` → `bool`
  - `operation.id` → `string`
  - `operation.last` → `bool`
  - `operation.producer` → `string`
  - `protoPayload.@type` → `string`
  - `protoPayload.authenticationInfo.principalEmail` → `string`
  - `protoPayload.methodName` → `string`
  - `protoPayload.requestMetadata.callerIp` → `string`
  - `protoPayload.requestMetadata.callerSuppliedUserAgent` → `string`
  - `protoPayload.resourceName` → `string`
  - `protoPayload.serviceName` → `string`
  - `protoPayload.status.code` → `datetime`
  - `protoPayload.status.message` → `string`
  - `receiveTimestamp` → `datetime`
  - `resource.labels.cluster_name` → `string`
  - `resource.type` → `string`
  - `timestamp` → `datetime`

#### 2. **Data Quality Assessment**
- **Missing values per column**:

| Column | Missing |
|--------|---------|
| labels.authorization.k8s.io/reason | 572 |

- **Duplicate rows:** 0  

#### 3. **Integration**
- Not performed in this workflow.

#### 4. **Aggregation**
- **Number of logs by decision:**

| Decision | Count |
|----------|-------|
| allow | 572 |
| forbid | 528 |

- **Number of logs by cluster:**

| Cluster | Count |
|---------|-------|
| nf-default | 255 |
| test-cluster | 221 |
| dev-cluster | 212 |
| staging-cluster | 210 |
| prod-cluster | 202 |

- **Number of logs by user:**

| User | Count |
|------|-------|
| service-account@company.iam.gserviceaccount.com | 227 |
| user@company.com | 225 |
| dev@company.com | 220 |
| system:anonymous | 216 |
| admin@company.com | 212 |

- **Number of logs by status code:**

| Status Code | Count |
|-------------|-------|
| 3 | 230 |
| 0 | 226 |
| 16 | 221 |
| 7 | 217 |
| 13 | 206 |

- **Number of logs by location:**

| Location | Count |
|----------|-------|
| europe-west1 | 304 |
| us-west1 | 283 |
| asia-southeast1 | 275 |
| us-central1 | 238 |

#### 5. **Sampling**
- Sampled 30% of the dataset
  
| insertId                     | labels.authorization.k8s.io/decision | resource.type | timestamp               |
|------------------------------|--------------------------------------|----------------|--------------------------|
| consolidated_event_329_995168 | allow                               | k8s_cluster    | 2024-08-24T13:23:09.0000Z |
| consolidated_event_689_975512 | forbid                              | k8s_cluster    | 2024-11-13T23:39:22.0000Z |
| consolidated_event_414_404737 | forbid                              | k8s_cluster    | 2024-08-18T04:11:39.0000Z |
| consolidated_event_789_927866 | allow                               | k8s_cluster    | 2024-11-27T23:15:04.0000Z |
| consolidated_event_245_725368 | allow                               | k8s_cluster    | 2024-04-11T06:27:51.0000Z |

#### 6. **Cleaning**
- Removes redundant columns and invalid entries.  
- Normalizes string fields and standardizes categorical data.

#### 7. **Handling Missing Values**
- Detects missing fields such as `principalEmail` or `reason`.  
- Imputes missing values using frequency-based methods.

#### 8. **Feature Engineering**
- **Resulted dataset example:**
  - Includes derived features: `method_action`, `service_short`, `resource_type_short`, `callerIp_is_private`, `callerIp_first_octet`, `receiveTimestamp` components, `timestamp` components.
  - Encoded categorical and binary fields for ML/analytics.

#### 9. **Discretization & Binarization**
- Converts boolean and categorical fields to binary format (e.g., `protoPayload.status.code__bin`, `callerIp_is_private__bin`, `insertId_*__bin`, `operation.id_*__bin`, `protoPayload.authenticationInfo.principalEmail_*__bin`, etc.)

#### 10. **Transformation**
- Standardizes and scales binary and numeric features (z-score normalization):
  - `protoPayload.status.code__bin__z`, `callerIp_is_private__bin__z`, `receiveTimestamp__month__bin__z`, `insertId_*__bin__z`, etc.

#### 11. **Dimensionality Reduction**
- Applies **PCA** on processed dataset:
  - `PCA_1, PCA_2, ..., PCA_10`
  - Captures main patterns in audit logs for further analysis or ML tasks.


## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/SuhejlaHoxha/PVDH_G6.git
cd PVDH_G6

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the preprocessing pipeline
python src/main.py
