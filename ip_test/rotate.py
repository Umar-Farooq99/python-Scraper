import random
import requests

# storing IPs from file to list
proxy_list = ['35.236.207.242:33333', '8.219.97.248:80']

# storing functional IPs in a list
working_proxies = []
for i in proxy_list:
    print(f"IP that is being checked: {i}")
    try:
        proxy = {
            'http': 'http://' + i,
            # 'https': 'http://' + i
        }
        response = requests.get('http://google.com', proxies=proxy)
        working_proxies.append(i)
    except:
        pass

print(f"Active IPs, {working_proxies}")

# rotating IPs from working_proxies considering we want to send 5 requests
for i in range(3):
    random_ip = random.choice(working_proxies)
    print(f"randam IP selected: {random_ip}")
    # rotating IPs from working_proxies
    proxy = {
        'http': 'http://' + random_ip,
        # 'https': 'http://' + random_ip
    }
    res = requests.get('http://ip.jsontest.com/', proxies=proxy)
    print(f"Request received from following IP:\n{res.text}")