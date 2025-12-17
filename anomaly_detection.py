import numpy as np
import matplotlib.pyplot as pt

#function to generate a data stream
def generate_data_stream(data_points=1000, time_window=50, random_noise_level=0.5):
    data_list = []
    for i in range(data_points):
        regular_pattern = np.sin(2*np.pi * i / time_window)
        noise = np.random.normal(0, random_noise_level)
        value = regular_pattern + noise
        data_list.append(value)

        #adding anomalies
        if np.random.rand() < 0.05:
            anomaly = value + np.random.uniform(5,10)
            data_list[-1] = anomaly
    return data_list

def anomaly_detection(data_stream, threshold=2):
    anomalies = []
    for i in range(len(data_stream)):
        if i < 30: continue

        mean = np.mean(data_stream[:i])
        standard_deviation = np.std(data_stream[:i])

        if standard_deviation == 0: continue

        z_score = (data_stream[i] - mean) / standard_deviation
        print("Z Score: ", z_score)
        if abs(z_score) > threshold:
            anomalies.append(i)
    return anomalies

#Step 3: create a function to visialize the data stream and anomalies
def visualize_data(data_stream, anomalies):
    pt.figure(figsize=(12, 6))
    pt.plot(data_stream, label='Data Stream', color='blue')
    pt.scatter(anomalies, [data_stream[i] for i in anomalies], color='red', label='Anomalies', zorder=5)
    pt.title('Data Stream with detected anomalies')
    pt.xlabel('Anomaly indices')
    pt.ylabel('Value')
    pt.legend()
    pt.grid()
    pt.show()

def main():
    data_points=1000
    data_stream = generate_data_stream(data_points)
    for i in range(len(data_stream)):
        print('Data Point: ', data_stream[i]) 
    anomalies = anomaly_detection(data_stream)
    print("Detected Anomalies: ", anomalies)
    visualize_data(data_stream, anomalies)

if __name__== "__main__":
    main()
