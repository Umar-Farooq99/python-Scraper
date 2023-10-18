import requests



proxy_List =[]
with open('free_proxy.txt') as f:
    for line in f:
        proxy_List.append(line.strip())
# print(proxy_List)
working_proxies =[]
for i in proxy_List:
    try:
        proxy ={
            'http': 'http://'+i,            #http://ip:port
            'https':'http://'+i
        }
        res = requests.get('https://example.org/',proxies=proxy)
        if res.status_code == 200:
           working_proxies.append(i)
    except requests.exceptions.RequestException as e:
      print(f"error with proxy{i}:{str(e)}")

print(f"working proxy:::{working_proxies}")