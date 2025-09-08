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

> [!NOTE]
> The application's metrics on the running system come under the host name “telegraf”. To view them, you should enter “telegraf” in the hostname field.

## Monitoring a different device on the local network

### Monitoring system metrics

To monitor system metrics on Linux and Windows operating systems, you must install the [telegraf](https://docs.influxdata.com/telegraf/v1/install/) service.
After installation, open the telegraf.conf and follow these steps:
  1. Find the [global_tags] section and add the line os_type = "the_operating_system_of_the_system_to_be_monitored" below it. 
     ```
        [global_tags]
  	      os_type = "the_operating_system_of_the_system_to_be_monitored"
     ```
  > [!WARNING]
  > The value of os_type must be either "linux" or "windows"
  
  2. Find the [agent] section and add the line hostname = "the_hostname_of_the_system_to_be_monitored" below it.
     ```
        [agent]
          hostname = "the_hostname_of_the_system_to_be_monitored"
     ```
  > [!IMPORTANT]
  > The hostname you enter to collect system metrics must be the same as the hostname you enter to collect logs.

  3. Find the [[outputs.influxdb_v2]] section and update this section according to the following code.
     ```
         urls = ["http://your_main_host_ip:8086"]
         token = "rSyrzmTBf3HRum2vtOuwCdbWYjHdZy3vut8zpwibaWxw1mFpg"
         organization = "docs"
         bucket = "home"
     ```
  > [!TIP]
  > These variables are available in the .env file. If you want to change the variables, you can change them via the .env file.

  4. (If you are using windows, you must follow this step) Find the [inputs.exec] section and add the line commands = ["powershell -ExecutionPolicy Bypass -File \"script_path""]
     ```
        [[inputs.exec]]
          commands = ["powershell -ExecutionPolicy Bypass -File \"script_path""]
     ```
  > [!NOTE]
  > This script counts all processes running on Windows operating systems and works on telegraf. This script is located within the telegraf directory. You must specify the path to the ps1 extension script in the script_path section. 

After all these settings, Telegram is restarted and system metrics become monitorable. The collected metrics are transferred to the InfluxDB database.


### Monitoring system logs

To monitör system logs on Linux and Windows operating systems, you should use two different services depending on the type of operating system.

If you are using a Linux system, you should follow the steps below:
  1. To collect system logs on Linux systems, the [filebeat service](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-installation-configuration) must be installed.
  2. After installation, open the filebeat.yml file.
  3. Add the following lines to the top of the file.
     ```
        name: your_hostname
	    tags: ["linux", "container"]
     ```
  > [!IMPORTANT]
  > The hostname you enter to collect system logs must be the same as the hostname you enter to collect metrics.
  4. Find the "output.logstash" section and add the line below it.
     ```
      output.logstash:
  	    hosts: ["your_main_host_ip:5044"]
  	    user: "logstash_internal"
  	    password: "${LOGSTASH_INTERNAL_PASSWORD}"
     ```
After all these settings, Filebeat is restarted and system logs become monitorable. The collected logs are transferred to the Kibana interface.

If you are using a Windows system, you should follow the steps below:
  1. To collect system logs on Windows systems, the [winlogbeat service](https://www.elastic.co/docs/reference/beats/winlogbeat/winlogbeat-installation-configuration) must be installed.
  2. After installation, open the winlogbeat.yml file.
  3. Find the "===General===" section and add the following line below it.
     ```
        name: "your_hostname"
        tags: ["windows"]
     ```
  > [!IMPORTANT]
  > The hostname you enter to collect system logs must be the same as the hostname you enter to collect metrics.
  4. Find the "output.logstash" section add add the line below it.
     ```
		output.logstash:
          hosts: ["your_main_host_ip:5044"]
     ```
After all these settings, Winlogbeat is restarted and system logs become monitorable. The collected logs are transferred to the Kibana interface.

After all these settings, different devices on the local network can be monitored.

### IMPORTANT NOTE
 If you running to application at WSL2 and you want to monitoring a different device, you should make portproxy for running application services.
 You should perform portproxy operations on ports 8086 (InfluxDB), 5000 (Web Application), 9200 (Elasticsearch), 5601 (Kibana) and 5044 (Logstash) on the device you wish to monitor. Below is a demonstration of how to perform this operation:
 ```
 	netsh interface portproxy add v4tov4 listenport=8086 listenaddress=0.0.0.0 connectport=8086 connectaddress=your_wsl2_ip;
 	netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=your_wsl2_ip;
 	netsh interface portproxy add v4tov4 listenport=9200 listenaddress=0.0.0.0 connectport=9200 connectaddress=your_wsl2_ip;
 	netsh interface portproxy add v4tov4 listenport=5601 listenaddress=0.0.0.0 connectport=5601 connectaddress=your_wsl2_ip;
 	netsh interface portproxy add v4tov4 listenport=5044 listenaddress=0.0.0.0 connectport=5044 connectaddress=your_wsl2_ip;
```
Sometimes, despite making these settings, you may not be able to access the service ports. You may need to delete the settings and make them again. This situation can happen frequently. You can use [](this script) for these like situations. This script creates a port proxy and security rule based on the ports you specify and the IP address you wish to redirect to. Through the same script, you can delete the port proxy and security rules you have created.
