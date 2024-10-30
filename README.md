# Anomaly Detection with Z-Score, EMA, and Seasonal Decomposition

## Overview
This project implements an anomaly detection system for streaming data using a combination of *Z-score, **Exponential Moving Average (EMA), and **Seasonal Decomposition*.
The system is designed to detect anomalies in real-time by checking for trends, seasonal patterns, and sudden changes in the data stream.
This project has 2 files; one with the brute force approach where I used the Z-Score statistical method to account for the anomalies, then I used *Z-score, **Exponential Moving Average (EMA), and **Seasonal Decomposition* approach helps identify unexpected deviations without mistaking regular patterns for anomalies.

## Approach
- *Z-Score*: Calculates how far each data point deviates from the recent mean while marking points that are significantly different. This provides a quick and effective way to flag outliers.
- *Exponential Moving Average (EMA)*: Smooths the data by giving more weight to the most recent values which helps the system to adapt to short-term trends and reduces the influence of older data (but not completely leaving it out).
- *Seasonal Decomposition*: Separates the data into trend, seasonal, and residual components. This prevents regular cycles or periodic changes from being flagged as anomalies, giving the approach more accuracy in detecting these anomalies.

## Why This Approach?
This combination offers a flexible and adaptive solution for data with short-term fluctuations and predictable seasonal patterns. Together the *Z-score, **Exponential Moving Average (EMA), and **Seasonal Decomposition*  ensure a robust anomaly detection mechanism suitable for data streaming.

## Usage
- Prerequisites: Git, Python(3.12)
- git clone https://github.com/Nelly-ayebale/anomaly_detection.git
- cd anomaly_detection
- set up virtual environment: python -m venv .venv 
- Install dependencies: python install matplotlib numpy pandas statsmodels
- Run the python anomaly_detection.py to see brute force approach results and python ema_zscore_detection.py to see results of *Z-score, **Exponential Moving Average (EMA), and **Seasonal Decomposition* approach.
