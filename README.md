# CarbonMeter: Data Center Carbon Footprint Calculator

CarbonMeter is an online tool to quickly assess carbon footprint of a data center. CarbonMeter relies on only two data points, namely data center area and power capacity, to estimate the number of servers, number of network devices and then estimates the manufacturing footprint, IT operational footprint, water usage, recycling impact. CarbonMeter is built using the popular "streamlit" library. 

## Parameters

- **Server Model**: Currently we support 3 server models with varying storage capacities: Dell R710, Dell R740, HPE ProLiant DL380
  
- **Power Capacity**: Total power capacity of a data center can be accessed from online resources, such as https://www.datacentermap.com.
  
- **Data Center Area**: Most data center providers publish data center area, and similarly this data point can be accessed from https://www.datacentermap.com.
  
- **PUE (Power usage effectiveness)**: PUE for most of the modern data centers ranges from 1.1 to 1.5, and 1.2 is generally accepted as a typical value.
  
- **Average System Utilization**
  
- **Per-rack-power**

- **Network Topology**

- **Port-per-Switch**
  
- **Energy Source Carbon Intensity**
  
- **IT Equipment Lifetime**
  
- **WUE (Water usage effectiveness)**

## Instructions

### Environment Setup
- Create a virtual environment
```
python -m venv myenv
```
- Install dependencies
```
pip install -r requirements
```

### Running CarbonMeter
You can run CarbonMeter with the following command:
```
streamlit run CarbonMeter
```
Running this command will automatically open up a browser window and will direct you to ```http://localhost:8501/```. Then you can adjust the parameters and visually observe the changes in estimations and plots. 