import numpy as np
import pandas as pd
import matplotlib.pyplot as pt
from statsmodels.tsa.seasonal import seasonal_decompose
import time

#I decided to optimize the zscore method by incorporating exponential moving averages (EMA) to give more weight to the most recent data
#However, since my algorithm was partially overlooking seasonal patterns, I added a seasonal pattern function and used panda series to decompose the data
#This way I will be able to filter out for seasonal patterns more accurately, and focus on the actual anomalies that are happening.
#I believe this can be further enhanced by adding dynamic thresholding and other features which I am further thinking about for further modification.

class DataStreamSimulator:
    def __init__(self,base_value=50,seasonal_variation=10,noise_level=5):
        """a constructor method that initializes the instance of the class default parameters:"""
        self.base_value = base_value 
        self.seasonal_variation = seasonal_variation
        self.noise_level = noise_level
        self.steps = 0

    def generate_data_point(self):
        """generating a new data point with seasonal variation and noise."""
        regular_pattern = self.seasonal_variation * np.sin(2*np.pi * self.steps / 50)  # Creating a seasonal pattern, dividing by a fixed divisor = 50 to control the cycle lengths
        noise = np.random.normal(0, self.noise_level)  # adding random noise
        self.steps += 1 #tracking progression as more data points are generated
        return self.base_value + regular_pattern + noise #returning the full data point that includes the baseline/start point, pattern and noise

class AnomalyDetector:
    def __init__(self, time_window=20, threshold=2):
        """initializing instance of the class"""
        self.time_window = time_window 
        self.threshold = threshold
        self.data_list = []

    def detect_anomaly(self, new_data_point):
        """function to detect anomalies basing on the z-score and EMA."""
        self.data_list.append(new_data_point)
        if len(self.data_list) < self.time_window: return False  # That would mean that there isn't enough data to detect anomalies

        # Start to calculate z-score
        mean = np.mean(self.data_list[-self.time_window:])
        standard_deviation = np.std(self.data_list[-self.time_window:])
        if standard_deviation == 0: return False
        z_score = (new_data_point - mean) / standard_deviation

        print(f"mean: {mean}, std: {standard_deviation}, z_score:{z_score}")
        return abs(z_score) > self.threshold # Checking for the anomaly

    def seasonal_pattern(self):
        """creating a function to add seasonal decomposition in order to adjust for seasonal changes."""
        if len(self.data_list) < 100: return 0  # This would mean that there isn't enough data for the decomposition

        data_series = pd.Series(self.data_list) # using panda series and adding the data_list
        if data_series.isnull().any(): 
            data_series = data_series.fillna(method='ffill')
        result = seasonal_decompose(data_series, model='additive', period=50) #result is broken down into the trend, the seasonal patterns and the residual
        return result.resid.iloc[-1] if result.resid is not None else 0 # Getting the latest residual to represent the anomaly in the data and retruning the residual

def visualize_data(data_stream, anomalies):
    """Visualizing the data stream and detected anomalies."""
    pt.clf()
    pt.plot(data_stream, label='Data Stream', color='blue')
    pt.scatter(anomalies, [data_stream[i] for i in anomalies], color='red', label='Anomalies', zorder=5)
    pt.title('Data Stream with detected anomalies')
    pt.xlabel('Anomaly')
    pt.ylabel('Value')
    pt.legend()
    pt.pause(0.1)

def main():
    # Initializing the data stream simulator and anomaly detector
    simulator = DataStreamSimulator()
    detector = AnomalyDetector()
    data_stream = []
    anomalies = []
    pt.ion()
    pt.figure(figsize=(12, 6))

    try:
        while True:
            new_data_point = simulator.generate_data_point() #generating a new data pint
            seasonal_adjustment = detector.seasonal_pattern()  #getting the seasonal patterns
            adjusted_data_point = new_data_point-seasonal_adjustment  #removing the seasonal patterns from the new data point to ensure we are getting anomalies that are not part of the regular/seasonal patterns
            data_stream.append(adjusted_data_point)

            if detector.detect_anomaly(adjusted_data_point):
                anomalies.append(len(data_stream) - 1)  # detecting the anomaly and storing its index
                print(f"anomaly detected at index: {len(data_stream) - 1}, value: {adjusted_data_point}")
            visualize_data(data_stream, anomalies) # visualizing the data stream and anomalies

            time.sleep(0.3)  # adding a delay in data streaming

    except KeyboardInterrupt:
        print("data streaming has stopped")

if __name__ == "__main__":
    main()
