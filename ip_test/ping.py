import os

# open free_proxy.txt file
with open('free_proxy.txt','r') as f:
    dump = f.read().splitlines()
    # print(dump)

# ping for each ip address
for ip in dump:
    res = os.popen(f'ping {ip}').read()
    if(('unreachable') or ('Request time out')) in res:
        print(res)
        f = open('output_proxy.txt', 'a')
        f.write(str(ip)+ 'is down'+ '\n')
        f.close()
    else:
       print(res)
       f = open('output_proxy.txt', 'a')
       f.write(str(ip)+ 'is up'+ '\n')
       f.close()
with open('output_proxy.txt') as file:
    output = file.read()
    print(output)