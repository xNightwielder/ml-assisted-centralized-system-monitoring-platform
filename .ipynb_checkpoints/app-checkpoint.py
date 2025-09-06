from flask import Flask, jsonify, render_template, request, redirect, url_for
from influxdb_client import InfluxDBClient
from elasticsearch import Elasticsearch
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import os

app = Flask(__name__)

# InfluxDB bağlantı bilgileri
INFLUX_URL = "http://localhost:8086"
TOKEN = "Era-SPBYXWBUo2sW0DR8jYflavLNGrxHX2VYCzFELbMgaRGLDBXfNcI3tK2IrDIk-Z_-I8r00pFWw95ZjGBjRg=="
ORG = "MyCompany"
BUCKET = "system_logs"

client = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
query_api = client.query_api()


# Elasticsearch Bağlantı Bilgileri
es = Elasticsearch("http://localhost:9200")

# InfluxDB'den veri çeken fonksiyonlar
def query_influxdb(metric,time_range,hostname):
    query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_cpu(metric, time_range,hostname):
    query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "cpu") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value(),
                "os_type": record.values.get("os_type")
            })
    return values

def query_influxdb_ram(metric, time_range,hostname):
    linux_query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "mem") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(linux_query)

    if all(len(table.records) == 0 for table in result):
        windows_query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "win_mem") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
        '''
        result = query_api.query(windows_query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_swap(metric, time_range,hostname):
    query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "swap") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_disk(metric, time_range,hostname):
    query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "disk") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_diskio(metric, time_range,hostname):
    query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "diskio") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_net(metric, time_range,hostname):
    linux_query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "net") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(linux_query)

    if all(len(table.records) == 0 for table in result):
        windows_query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "win_net") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
        '''
        result = query_api.query(windows_query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_system(metric, time_range,hostname):
    query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "system") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value()
            })
    return values

def query_influxdb_process(metric, time_range,hostname):
    linux_query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "processes") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
    '''
    result = query_api.query(linux_query)

    if all(len(table.records) == 0 for table in result):
        windows_query = f'''from(bucket: "{BUCKET}") |> range(start: -{time_range}) |> filter(fn: (r) => r._measurement == "win_system") |> filter(fn: (r) => r._field == "{metric}") |> filter(fn: (r) => r["host"] == "{hostname}")
        '''
        result = query_api.query(windows_query)

    values = []
    for table in result:
        for record in table.records:
            values.append({
                "time": record.get_time(),
                "metric": metric,
                "field": record.get_field(),
                "value": record.get_value(),
            })
    return values

@app.route("/dashboard")
def dashboard():
    hostname = request.args.get("hostname", "")
    if not hostname:
        return redirect("/")  # hostname yoksa form sayfasına geri döndür

    return render_template("index.html", hostname=hostname)

@app.route('/metrics/<time_range>', methods=['GET'])
def get_metrics(time_range):
    hostname = request.args.get("hostname", "")
    metrics = {
        "cpu_user": query_influxdb_cpu("usage_user", time_range, hostname),
        "cpu_system": query_influxdb_cpu("usage_system", time_range, hostname),
        "cpu_idle": query_influxdb_cpu("usage_idle", time_range, hostname),
        "cpu_io": query_influxdb_cpu("usage_iowait", time_range, hostname),
        "mem_total": query_influxdb_ram("total", time_range, hostname),
        "mem_used": query_influxdb_ram("used", time_range, hostname),
        "mem_available": query_influxdb_ram("available", time_range, hostname),
        "mem_used_percent": query_influxdb_ram("used_percent", time_range, hostname),
        "mem_cached": query_influxdb_ram("cached", time_range, hostname),
        "mem_cached_win": query_influxdb_ram("Standby_Cache_Normal_Priority_Bytes", time_range, hostname),
        "swap_total": query_influxdb_swap("total", time_range, hostname),
        "swap_used": query_influxdb_swap("used", time_range, hostname),
        "swap_free": query_influxdb_swap("free", time_range, hostname),
        "swap_used_percent": query_influxdb_swap("used_percent", time_range, hostname),
        "disk_total": query_influxdb_disk("total", time_range, hostname),
        "disk_used": query_influxdb_disk("used", time_range, hostname),
        "disk_free": query_influxdb_disk("free", time_range, hostname),
        "disk_used_percent": query_influxdb_disk("used_percent", time_range, hostname),
        "diskio_read": query_influxdb_diskio("read_bytes", time_range, hostname),
        "diskio_write": query_influxdb_diskio("write_bytes", time_range, hostname),
        "diskio_time": query_influxdb_diskio("io_time", time_range, hostname),
        "diskio_ms": query_influxdb_diskio("io_await", time_range, hostname),
        "bytes_recv": query_influxdb_net("bytes_recv", time_range, hostname),
        "bytes_recv_persec": query_influxdb_net("Bytes_Received_persec", time_range, hostname),
        "bytes_sent": query_influxdb_net("bytes_sent", time_range, hostname),
        "bytes_sent_persec": query_influxdb_net("Bytes_Sent_persec", time_range, hostname),
        "packets_recv": query_influxdb_net("packets_recv", time_range, hostname),
        "packets_recv_persec": query_influxdb_net("Packets_Received_persec", time_range, hostname),
        "packets_sent": query_influxdb_net("packets_sent", time_range, hostname),
        "packets_sent_persec": query_influxdb_net("Packets_Sent_persec", time_range, hostname),
        "err_in": query_influxdb_net("err_in", time_range, hostname),
        "err_in_received": query_influxdb_net("Packets_Received_Errors", time_range, hostname),
        "err_out": query_influxdb_net("err_out", time_range, hostname),
        "err_out_outbound": query_influxdb_net("Packets_Outbound_Errors", time_range, hostname),
        "drop_in": query_influxdb_net("drop_in", time_range, hostname),
        "drop_in_received": query_influxdb_net("Packets_Received_Discarded", time_range, hostname),
        "drop_out": query_influxdb_net("drop_out", time_range, hostname),
        "drop_out_outbound": query_influxdb_net("Packets_Outbound_Discarded", time_range, hostname),
        "n_cpus": query_influxdb_system("n_cpus", time_range, hostname),
        "load1": query_influxdb_system("load1", time_range, hostname),
        "load5": query_influxdb_system("load5", time_range, hostname),
        "load15": query_influxdb_system("load15", time_range, hostname),
        "process_thread": query_influxdb_process("total_threads", time_range, hostname),
        "process_thread_win": query_influxdb_process("Threads", time_range, hostname),
        "process_total": query_influxdb_process("total", time_range, hostname),
        "process_total_win": query_influxdb_process("Processes", time_range, hostname),
        "process_running": query_influxdb_process("running", time_range, hostname),
        "process_running_win": query_influxdb_process("cpu_active_count", time_range, hostname),
        "process_blocked": query_influxdb_process("blocked", time_range, hostname),
        "process_zombies": query_influxdb_process("zombies", time_range, hostname),
    }
    
    #print(metrics["cpu_user"][-1])
    #print(metrics["cpu_user"])
    print(metrics["cpu_user"][-1]["os_type"])
    
    if metrics["cpu_user"][-1]["os_type"] != "windows":
      df = pd.DataFrame(
        {
          'cpu_user': metrics["cpu_user"][-1]["value"],
          'cpu_system': metrics["cpu_system"][-1]["value"],
          'cpu_idle': metrics["cpu_idle"][-1]["value"],
          'cpu_io': metrics["cpu_io"][-1]["value"],
          'mem_total': metrics["mem_total"][-1]["value"],
          'mem_used': metrics["mem_used"][-1]["value"],
          'mem_available': metrics["mem_available"][-1]["value"],
          'mem_used_percent': metrics["mem_used_percent"][-1]["value"],
          'mem_cached': metrics["mem_cached"][-1]["value"],
          #'mem_cached_win': metrics["mem_cached_win"][-1]["value"],
          'swap_total': metrics["swap_total"][-1]["value"],
          'swap_used': metrics["swap_used"][-1]["value"],
          'swap_free': metrics["swap_free"][-1]["value"],
          'swap_used_percent': metrics["swap_used_percent"][-1]["value"],
          'disk_total': metrics["disk_total"][-1]["value"],
          'disk_used': metrics["disk_used"][-1]["value"],
          'disk_free': metrics["disk_free"][-1]["value"],
          'disk_used_percent': metrics["disk_used_percent"][-1]["value"],
          'diskio_read': metrics["diskio_read"][-1]["value"],
          'diskio_write': metrics["diskio_write"][-1]["value"],
          'diskio_time': metrics["diskio_time"][-1]["value"],
          'diskio_ms': metrics["diskio_ms"][-1]["value"],
          'bytes_recv': metrics["bytes_recv"][-1]["value"],
          'bytes_sent': metrics["bytes_sent"][-1]["value"],
          'packets_recv': metrics["packets_recv"][-1]["value"],
          'packets_sent': metrics["packets_sent"][-1]["value"],
          'err_in': metrics["err_in"][-1]["value"],
          'err_out': metrics["err_out"][-1]["value"],
          'drop_in': metrics["drop_in"][-1]["value"],
          'drop_out': metrics["drop_out"][-1]["value"],
          'load1': metrics["load1"][-1]["value"],
          'load5': metrics["load5"][-1]["value"],
          'load15': metrics["load15"][-1]["value"],
          'process_thread': metrics["process_thread"][-1]["value"],
          'process_total': metrics["process_total"][-1]["value"],
          'process_running': metrics["process_running"][-1]["value"],
          'process_blocked': metrics["process_blocked"][-1]["value"],
          'process_zombies': metrics["process_zombies"][-1]["value"],
        }, index=[0])
        
      filename = "system-metrics-" + hostname + ".csv"
        
      if not os.path.isfile(filename):
          df.to_csv(filename, index=False, mode='w')
      else:
          df.to_csv(filename, index=False, mode='a', header=False)

      

    else:
        df = pd.DataFrame(
          {
            'cpu_user': metrics["cpu_user"][-1]["value"],
            'cpu_system': metrics["cpu_system"][-1]["value"],
            'cpu_idle': metrics["cpu_idle"][-1]["value"],
            'cpu_io': metrics["cpu_io"][-1]["value"],
            'mem_total': metrics["mem_total"][-1]["value"],
            'mem_used': metrics["mem_used"][-1]["value"],
            'mem_available': metrics["mem_available"][-1]["value"],
            'mem_used_percent': metrics["mem_used_percent"][-1]["value"],
            'mem_cached_win': metrics["mem_cached_win"][-1]["value"],
            'swap_total': metrics["swap_total"][-1]["value"],
            'swap_used': metrics["swap_used"][-1]["value"],
            'swap_free': metrics["swap_free"][-1]["value"],
            'swap_used_percent': metrics["swap_used_percent"][-1]["value"],
            'disk_total': metrics["disk_total"][-1]["value"],
            'disk_used': metrics["disk_used"][-1]["value"],
            'disk_free': metrics["disk_free"][-1]["value"],
            'disk_used_percent': metrics["disk_used_percent"][-1]["value"],
            'diskio_read': metrics["diskio_read"][-1]["value"],
            'diskio_write': metrics["diskio_write"][-1]["value"],
            'diskio_time': metrics["diskio_time"][-1]["value"],
            'diskio_ms': metrics["diskio_ms"][-1]["value"],
            'bytes_recv_persec': metrics["bytes_recv_persec"][-1]["value"],
            'bytes_sent_persec': metrics["bytes_sent_persec"][-1]["value"],
            'packets_recv_persec': metrics["packets_recv_persec"][-1]["value"],
            'packets_sent_persec': metrics["packets_sent_persec"][-1]["value"],
            'err_in_received': metrics["err_in_received"][-1]["value"],
            'err_out_outbound': metrics["err_out_outbound"][-1]["value"],
            'drop_in_received': metrics["drop_in_received"][-1]["value"],
            'drop_out_outbound': metrics["drop_out_outbound"][-1]["value"],
            'load1': metrics["load1"][-1]["value"],
            'load5': metrics["load5"][-1]["value"],
            'load15': metrics["load15"][-1]["value"],
            'process_thread_win': metrics["process_thread_win"][-1]["value"],
            'process_total_win': metrics["process_total_win"][-1]["value"],
            'process_running_win': metrics["process_running_win"][-1]["value"],
        }, index=[0])

        def classify_system(cpu_user, cpu_system, cpu_idle, mem_used_percent, swap_used_percent, load1, load5, load15, disk_used_percent, drop_in_received, drop_out_outbound):

            score = 0

            if cpu_user + cpu_system < 30:
                score += 0
            elif cpu_user + cpu_system < 70:
                score += 1
            elif cpu_user + cpu_system < 90:
                score += 2
            else:
                score += 3


            if mem_used_percent < 30:
                score += 0
            elif mem_used_percent < 70:
                score += 1
            elif mem_used_percent < 90:
                score += 2
            else:
                score += 3

            if swap_used_percent < 10:
                score += 0
            elif swap_used_percent < 20:
                score += 1
            elif swap_used_percent < 30:
                score += 2
            else:
                score += 3

            if load1 / metrics["n_cpus"][-1]["value"] < 0.1:
                score += 0
            elif load1 / metrics["n_cpus"][-1]["value"] < 0.7:
                score += 1
            elif load1 / metrics["n_cpus"][-1]["value"] <= 1:
                score += 2
            else:
                score += 3

            if load5 / metrics["n_cpus"][-1]["value"] < 0.1:
                score += 0
            elif load5 / metrics["n_cpus"][-1]["value"] < 0.7:
                score += 1
            elif load5 / metrics["n_cpus"][-1]["value"] <= 1:
                score += 2
            else:
                score += 3

            if load15 / metrics["n_cpus"][-1]["value"] < 0.1:
                score += 0
            elif load15 / metrics["n_cpus"][-1]["value"] < 0.7:
                score += 1
            elif load15 / metrics["n_cpus"][-1]["value"] <= 1:
                score += 2
            else:
                score += 3

            if disk_used_percent < 70:
                score += 0
            elif disk_used_percent < 80:
                score += 1
            elif disk_used_percent < 95:
                score += 2
            else:
                score += 3

            if drop_in_received == 0:
                score += 0
            else:
                score += 3

            if drop_out_outbound == 0:
                score += 0
            else:
                score += 3


            print(score)
            
            if score <=5:
                return "boşta"
            elif score <= 11:
                return "normal"
            elif score <= 18:
                return "yüksek uyarı"
            else:
                return "kritik uyarı"




        
        df["system_label"] = df.apply(
            lambda row: classify_system(metrics["cpu_user"][-1]["value"], metrics["cpu_system"][-1]["value"], metrics["cpu_idle"][-1]["value"], metrics["mem_used_percent"][-1]["value"], metrics["swap_used_percent"][-1]["value"], metrics["load1"][-1]["value"], metrics["load5"][-1]["value"], metrics["load15"][-1]["value"], metrics["disk_used_percent"][-1]["value"], metrics["drop_in_received"][-1]["value"], metrics["drop_out_outbound"][-1]["value"]),
            axis=1
        )

        
        filename = "system-metrics-" + hostname + ".csv"
        
        if not os.path.isfile(filename):
            df.to_csv(filename, index=False, mode='w')
        else:
            df.to_csv(filename, index=False, mode='a', header=False)



        df = pd.read_csv("system-metrics-" + hostname + "2.csv", sep=',')
        print(df.head())

        selected_features = ['cpu_user', 'cpu_system', 'mem_used_percent', 'swap_used_percent', 'load1', 'load5', 'load15', 'disk_used_percent', 'drop_in_received', 'drop_out_outbound', 'diskio_ms' ]
        X = df[selected_features]
        y = df["system_label"]

        le = LabelEncoder()
        y = le.fit_transform(y)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')

        print("Doğruluk Skorları:", scores)
        print("Ortalama Doğruluk:", np.mean(scores))

        # Son bir test için veriyi ayırma (çapraz doğrulama yapıyorsanız bu adım opsiyonel)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Final modeli
        final_model = RandomForestClassifier(n_estimators=100, random_state=42)
        final_model.fit(X_train, y_train)

        # Test skoru
        print("Test Doğruluğu:", final_model.score(X_test, y_test))

        y_pred = final_model.predict(X_test)
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        labels = final_model.classes_
        cm = confusion_matrix(y_test,y_pred,labels=labels)
        

        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
        plt.xlabel("Tahmin Edilen Etiket")
        plt.ylabel("Gerçek Etiket")
        plt.title("Confusion Matrix")
        plt.show()


        



    return jsonify(metrics)

# Elasticsearch

# Elasticsearch'tan logları alan API fonksiyonu
@app.route('/logs', methods=['GET'])
def get_logs():
    hostname = request.args.get("hostname", "")

    winlogs = []
    linuxlogs = []

    query = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "term": { "host.hostname": hostname },
                    }
                ]
                
            }
        },
        "size": 100,
        "sort": [{"@timestamp": {"order": "desc"}}]
        #"_source": ["event", "agent", "winlog", "tags"],
    }


    win_result = es.search(index="win-system-logs-*", body=query)
    linux_result = es.search(index="linux-system-logs-*", body=query)
    
    if win_result["hits"]["hits"] and "windows" in win_result["hits"]["hits"][0]["_source"]["tags"]:
        for hit in win_result["hits"]["hits"]:

            winlogs.append({
                "timestamp": hit["_source"]["event"].get("created"),
                "host": hit["_source"]["agent"].get("name", ""),
                "program": hit["_source"]["event"].get("provider", ""),
                "programID": hit["_source"]["winlog"]["process"].get("pid", ""),
                "message": hit["_source"]["event"].get("original", "").strip()
            })
        return jsonify(winlogs)
    else:
        if linux_result["hits"]["hits"] and "linux" in linux_result["hits"]["hits"][0]["_source"]["tags"]:
            for hit in linux_result["hits"]["hits"]:
                if hit["_source"].get("syslog_program") != "filebeat":
                    linuxlogs.append({
                        "timestamp": hit["_source"].get("syslog_timestamp"),
                        "host": hit["_source"].get("syslog_hostname", "N/A"),
                        "program": hit["_source"].get("syslog_program", "").split("[")[0],
                        "programID": hit["_source"].get("syslog_pid", ""),
                        "message": hit["_source"].get("syslog_message", "").strip()
                    })

                elif hit["_source"].get("syslog_program") == "filebeat":
                    linuxlogs.append({
                        "timestamp": hit["_source"].get("syslog_timestamp"),
                        "host": hit["_source"].get("syslog_hostname", "N/A"),
                        "program": hit["_source"].get("syslog_program", "").split("[")[0],
                        "programID": hit["_source"].get("syslog_pid", ""),
                        "message": hit["_source"]["parsed_json"].get("message", "").strip()
                    })

            return jsonify(linuxlogs)


    
    
    
   
        
    
    




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("hostname.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)