# 🛡️ FraudShield AI — Banking Fraud Detection System

A real-time **credit card fraud detection** web app built with **Streamlit** and powered by a **LightGBM** machine learning model.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-FF4B4B?logo=streamlit)
![LightGBM](https://img.shields.io/badge/LightGBM-4.5.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

FraudShield AI analyzes credit card transactions and predicts whether they are **fraudulent or legitimate** in real time. It uses a trained LightGBM classifier alongside geospatial distance features to deliver fast, accurate predictions.

---

## ✨ Features

- 🔍 **Real-time Fraud Detection** — instant predictions with confidence scores
- 📍 **Auto-detect Location** — fills coordinates via IP geolocation
- 🗺️ **Location Analysis** — computes distance between cardholder & merchant; shows map
- 📋 **Transaction History** — session-based sidebar history with fraud/safe indicators
- 🎨 **Modern UI** — clean card-based layout with animated confidence bars

---

## 🧠 ML Model

| Property | Detail |
|---|---|
| **Algorithm** | LightGBM (Gradient Boosted Trees) |
| **Input Features** | Merchant, Category, Amount, Distance, Hour, Day, Month, Gender, CC Number (hashed) |
| **Output** | Binary classification — Fraud (1) / Legitimate (0) + probability score |
| **Artifacts** | `fraud_detection_model.jb`, `label_encoder.jb` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/nitinvedi/Banking_Fraud_Detection_System.git
cd Banking_Fraud_Detection_System
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 📁 Project Structure

```
Banking_Fraud_Detection_System/
├── app.py                    # Main Streamlit application
├── fraud_detection_model.jb  # Trained LightGBM model
├── label_encoder.jb          # Label encoders for categorical features
├── requirements.txt          # Python dependencies
└── img-overview.png          # App overview screenshot
```

---

## 📦 Dependencies

```
streamlit==1.41.1
pandas==2.2.3
joblib==1.4.2
requests==2.32.3
geopy==2.4.1
lightgbm==4.5.0
numpy==2.2.2
scikit-learn==1.6.1
```

---

## 👥 Team

| Name | ID |
|---|---|
| Nitin Chaturvedi | 12306849 |
| Aditi Verma | 12307076 |
| Mansi Singh | 12306194 |

---

## ⚠️ Disclaimer

This application is built for **educational purposes**. Credit card numbers are hashed client-side and are never stored or transmitted. Do not use real card data.

---

<p align="center">FraudShield AI · v2.0 · Powered by LightGBM</p>
