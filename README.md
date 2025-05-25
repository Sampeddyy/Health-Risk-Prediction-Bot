# Health-Risk-Prediction-Bot
# 🏥 Health-Risk-Prediction-Bot

An intelligent system that analyzes user health data and predicts potential risks using machine learning and predefined thresholds — capable of generating advice and reports based on symptoms and diagnostics.

![Python](https://img.shields.io/badge/built_with-python-blue?logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 🩺 Overview

This bot uses a trained ML model to assess symptoms, daily intake, and user metrics to predict possible diseases and health risks. Additional modules simulate diagnostic behavior similar to real-world health consultations.

---

## 📁 Folder Structure

| File / Folder                | Description                                            |
|-----------------------------|--------------------------------------------------------|
| `Main.py`                   | Main app entry logic and routing                       |
| `medicalreport.py`          | Generates medical-like reports                         |
| `disease_model_tf.keras`    | Pre-trained ML model for disease prediction            |
| `disease_dataset.csv`       | Dataset used for training model                        |
| `predict_diseases_with_advice.py` | Predicts diseases with advice                   |
| `dieseasetable.py`          | Static disease reference logic                         |
| `dailyintakediet.py`        | Nutrition-based dietary logic                          |
| `data.py`, `info.py`, etc.  | Helper modules                                         |
| `audio_output/`             | Output audio advice (if TTS used)                      |
| `Person Calories Data/`     | Structured individual intake records                   |
| `requirements.txt`          | Python dependencies                                    |
| `LICENSE`                   | MIT License                                            |

---

## 🧠 Core Concepts

- Medical Diagnosis Simulation  
- Supervised Machine Learning  
- Health Metric Tracking  
- Automated Dietary Recommendations  

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python Main.py
