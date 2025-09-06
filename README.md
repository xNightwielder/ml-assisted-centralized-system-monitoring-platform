# Machine Learning-Supported Centralized System Monitoring Platform

A web platform that monitors system metrics on Linux and Windows systems and uses machine learning to predict the system's status.

## Features

* Compatibility with Linux and Windows operating systems
* Ability to monitor system metrics such as CPU, RAM, disk, network, and load average
* Data collected up to 24 hours can be tracked via the graph
* The system's ability to predict its current state

## Technologies
* Frontend: JavaScript, HTML, CSS, Chart.js
* Backend: Python (Flask), Scikit-learn, Pandas
* Monitoring & Logging: ELK Stack (Elasticsearch, Logstash, Kibana), Telegraf
* Containerization: Docker
* Database: InfluxDB
* Environment: Linux

## Requirements
* Docker

## Usage

1. Clone the repository:
 ```bash
   git clone https://github.com/xNightwielder/ml-assisted-centralized-system-monitoring-platform.git
   cd ml-assisted-centralized-system-monitoring-platform
```
2. Run the following codes in order
```
  docker compose up setup
  docker compose up
```
## Monitoring a different device on the local network
If your system is windows:
  1. To monitor system metrics, you need to install the “telegraf” service on the device you want to monitor.


## Important Notes
* The application's metrics on the running system come under the host name “telegraf”. To view them, you should enter “telegraf” in the username field.
