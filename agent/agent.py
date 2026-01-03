import time
import psutil
import platform
import requests
import json

#CONFIG
DRY_RUN = False 

#Flask-server
SERVER_URL = "http://localhost:5001/api/metrics" 

#Uppdaterings tid
INTERVAL = 10 

def get_system_metrics():
    """Samlar in data från OS"""
    
    #datorns nätverksnamn
    hostname = platform.node()
    
    #CPU-användning
    cpu_percent = psutil.cpu_percent(interval=1)
    
    #RAM-minne
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    
    #Diskanvändning
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    #Skapa objekt med datan
    metrics_payload = {
        "hostname": hostname,
        "cpu_usage": cpu_percent,
        "ram_usage": ram_percent,
        "disk_usage": disk_percent
    }
    
    return metrics_payload

def run_agent():
    print(f"Startar övervakningsagent på {platform.node()}...")
    print(f"Intervall: {INTERVAL} sekunder\n")

    while True:
        try:
            #Hämta data
            data = get_system_metrics()
            
            if DRY_RUN:
                #TEST
                print(f"[DRY RUN] Data insamlad: {json.dumps(data, indent=2)}")
            else:
                #POST req
                response = requests.post(SERVER_URL, json=data, timeout=5)
                
                if response.status_code == 201:
                    print(f"Data skickad: CPU {data['cpu_usage']}% | RAM {data['ram_usage']}%")
                else:
                    print(f"Serverfel: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("Kunde inte nå servern. Är backend igång?")
        except Exception as e:
            print(f"Ett oväntat fel uppstod: {e}")

        # Vänta innan nästa mätning
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run_agent()