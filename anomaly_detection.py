# This is the BRUTE FORCE APPROACH of the problem:
# Initialize an empty list that is going to be responsible for the data stream
# - for each new entry of a data point in the stream, I will:
# ---add that data point to the data stream
# ---calculate the mean and standard deviation of the data stream within a window
# ---calculate the z-score for the new data point entry
# ---finally, if the z-score exceed the threshold, then it will be flagged as an anomaly
# --repeat steps#

# Step 1: creating a function that generates a continuous data stream, incorportating regular patterns, seasonal elements and random noise.

import numpy as np
import matplotlib.pyplot as pt

#function to generate a data stream
def generate_data_stream(data_points=1000, time_window=50, random_noise_level=0.5):
    data_list = []
    for i in range(data_points):
        regular_pattern = np.sin(2*np.pi * i / time_window) #this creates a sine wave, with a repeating full cycle for each data point over the total time period that is set 
        noise = np.random.normal(0, random_noise_level) #this adds the random noise
        value = regular_pattern + noise #creating a total value that takes in the regular pattern + the random noise to create data points that follow a trend but with randomness
        data_list.append(value) #appending the value as a data point in the data_list

        #adding anomalies
        if np.random.rand() < 0.05: # adding an anomaly rate chance of 5%
            anomaly = value + np.random.uniform(5,10) #incase an anomaly does happen then I want it to get boosted by a random amount between 5 and 10, to make it stand out from the regular pattern
            data_list[-1] = anomaly # replacing the last entry in the data list with the anomalous one
    return data_list

#Step 2: creating a function to flag anomalies as the data is being streamed
def anomaly_detection(data_stream, threshold=2):
    anomalies = []
    for i in range(len(data_stream)):
        if i < 30: continue # ensuring that we have a decent amount of data points to evaluate what 'normal' looks like

        mean = np.mean(data_stream[:i]) #calculating mean of all previous data points until i
        standard_deviation = np.std(data_stream[:i]) #calculating standard deviation of all previous data points until i

        if standard_deviation == 0: continue #skipping in order to avoid dividing by 0

        z_score = (data_stream[i] - mean) / standard_deviation #using the z-score formular to get the z_score
        print("Z Score: ", z_score)
        if abs(z_score) > threshold:
            anomalies.append(i) #if the absolute value of the z_score is greater than the threshold then that data point is flagged as an anomaly and its index stored in the anomalies list
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