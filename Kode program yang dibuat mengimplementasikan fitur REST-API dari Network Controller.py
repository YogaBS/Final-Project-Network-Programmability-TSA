# Ijmport library yang dibutuhkan
import json
import requests
from time import *

# Menambahkan base_url, serta autentikasi user dan password untuk masuk ke website sdn
base_url = "http://localhost:58001/api/v1"
user = "cisco"
password = "cisco123"

# Fungsi untuk mendapatkan ticket rest API
def get_ticket():
    # Menentukan header dan data yang dibutuhkan untuk login
    headers = {"content-type": "application/json"}
    data = {"username": user, "password": password}
    # Membuat wadah untuk melakukan requests post untuk meminta ticket dalam bentuk json
    response = requests.post(base_url+"/ticket", headers=headers, json=data)
    ticket = response.json()
    # Parsing data untuk mendapatkan ticket
    service_ticket = ticket["response"]["serviceTicket"]
    return service_ticket

# Fungsi untuk menghitung managed device yang terdeteksi/terkoneksi
def get_network_device_count():
    ticket = get_ticket()
    headers = {"X-Auth-Token": ticket}
    response = requests.get(base_url+"/network-device/count", headers=headers)
    managed_device_count = response.json()
    print("Total Managed Device :", managed_device_count["response"])

# Fungsi untuk mendapatkan list managed network device yang terkoneksi dengan SDN
def get_network_device():
    ticket = get_ticket()
    headers = {"X-Auth-Token": ticket}
    response = requests.get(base_url+"/network-device", headers=headers)
    print("===Mendapatkan Daftar Managed Device===")
    print("Status Code : ",response.status_code)
    managed_device = response.json()
    networkDevices = managed_device["response"]

    for networkDevice in networkDevices:
        print(networkDevice["hostname"], "\t\t", networkDevice["platformId"], "\t", networkDevice["managementIpAddress"])

# Fungsi untuk mendapatkan list host yang tersambung dengan jaringan
def get_connected_hosts():
    ticket = get_ticket()
    headers = {"X-Auth-Token": ticket}
    response = requests.get(base_url+"/host", headers=headers, verify=False)
    print("===Mendapatkan Daftar Host===")
    print("Status Code : ",response.status_code)
    connectedDevices = response.json()
    devices = connectedDevices["response"]
    print("Device Name \t IP Address \t MAC Address \t Connected Port")
    for device in devices:
        print(device["hostName"], "\t", device["hostIp"], "\t", device["hostMac"], "\t\t", device["connectedInterfaceName"])

# Membuat fungsi untuk monitoring kesehatan jaringan
def get_network_health():
    ticket = get_ticket()
    headers = {"X-Auth-Token": ticket}
    response = requests.get(base_url+"/assurance/health", headers=headers)
    health = response.json()
    network_health = health['response'][0]['networkDevices']['totalPercentage']
    return network_health

# Membuat fungsi untuk mendapatkan informasi masalah yang terdapat pada jaringan yang dimontiroing
def get_network_issues():
    ticket = get_ticket()
    headers = {'Accept': 'application/yang-data+json', 'X-Auth-Token': ticket}
    issues = requests.get(url = base_url + "/assurance/health-issues", headers=headers)
    issue_details = issues.json()
    devices = len(issue_details['response'])
    output = "Peringatan! Terjadi gangguan akses ke "+ str(devices) +" perangkat berikut:\n"
    output += "-"*60 +"\n"
    output += "NO. | PERANGKAT | WAKTU | DESKRIPSI\n"
    output +="-"*60 +"\n"
    number=1
    for device in issue_details['response']:
        output += ""+ str(number) +". | "+ device['issueSource'] +" | "+ device['issueTimestamp'] +" | "+ device['issueDescription'] +"\n"
        number +=1
    return output

if __name__ == "__main__":
    print("===================================================================================")
    print("==============MONITORING JARINGAN MENGGUNAKAN SDN CONTROLLER REST API==============")
    print("===================FINAL PROJECT DTS-TSA NETWORK PROGRAMMABILITY===================")
    print("========================YOGA BAYU SETIAWAN/1810501014=======================")
    print("===================================================================================")
    print("Kode REST API : " + get_ticket())
    get_network_device_count()
    get_network_device()
    get_connected_hosts()
    network_health = get_network_health()
    if int(network_health) < 100:
        issues = get_network_issues()
        print(issues)
    else:
        print("Persentase Network Health: "+ network_health +"%")
    