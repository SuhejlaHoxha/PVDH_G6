# PVDH_G6

**Authors:** Suhejla Hoxha (suhejla.hoxha@student.uni-pr.edu), Dredhza Braina (dredhza.braina@student.uni-pr.edu), Art Ukshini (art.ukshini@student.uni-pr.edu)

## Introduction

This repository represents a development which in itself contains a dataset extracted from GCP (Google Cloud Platform), a cloud provider, which nowadays is used widely across the world, offering various services and environments for enterprises. This dataset is filled with logs extracted from **LIVE** environments in real world, such as K8S (Kubernetes) from GKE (Google Kubernetes Engine). In this dataset there is activity found in the *wild*, where potentially malicious behaviour can be seen.

Huge datasets such as this one, require certain efforts to make it useful in order to perform various activities and analysis. What our group has done with this dataset is:

### Data preprocessing
- 1) **Preprocessing for preparing data for analysis.**
- 2) **Data collection, definition of data types, and data quality.**
- 3) **Integration, aggregation, sampling, cleaning, identification, and strategy for handling missing values.**
- 4) **Dimensionality reduction, feature subset selection, feature creation, discretization and binarization, transformation.**

## Usage instructions

>```bash
># Clone repo locally
>git clone https://github.com/SuhejlaHoxha/PVDH_G6.git
>```


>```bash
># Install required dependencies
>python3 -m pip install -r requirements.txt
>```


>```bash
># Run
>python3 main.py
>```

