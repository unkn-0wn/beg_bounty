#!/usr/bin/env python
import sys, socket, json, requests, ipaddress
print("Resolving Domin into IP and removing CDN's")

# variables
domain_list = open(sys.argv[1], 'r').readlines()
ip_list , blacklist_ip, blacklist_networks , final_list = [], [], [], []

# cloudflare blacklisted ip's
blacklist_networks = [ip for ip in requests.get(url='https://www.cloudflare.com/ips-v4').text.split("\n") if ip != '']

# cloudfront blacklisted ip's
res = requests.get(url='http://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips').json()
blacklist_networks += res['CLOUDFRONT_GLOBAL_IP_LIST']
blacklist_networks += res['CLOUDFRONT_REGIONAL_EDGE_IP_LIST']

# get ip from CIDR
for blacklist_network in blacklist_networks:
    blacklist_ip += [str(ip) for ip in ipaddress.IPv4Network(blacklist_network)]

# read input domain list, and get their ip
for domain in domain_list:
    try:
        ip_list.append(socket.gethostbyname(domain.replace("http://", "").replace("https://", "").replace(" ", "").replace("\n", "")))
    except socket.gaierror:
        print(a)
        pass

# remove CDN ip's
final_list = list(set([ip for ip in ip_list if ip not in blacklist_ip]))

# write output
outfile = f'{sys.argv[1]}'.replace('.txt', '_resolved.txt')
with open(outfile, 'w') as f:
    for ip in final_list:
        f.write(f'{ip}\n')
