#! /usr/bin/python

WEB_SERVER_ACCESS_LOG_FILE = 'xxx.log'
OUTPUT_UNIQUE_IPS_LIST_FILE = 'IPs.log'

f = open(WEB_SERVER_ACCESS_LOG_FILE)
l = f.readlines()
ips = [i.partition(' ')[0] for i in l]

# get unique IPs
s = set(ips)
f.close()

# write IPs to file
f = open(OUTPUT_UNIQUE_IPS_LIST_FILE, 'w')
for i in s:
    f.write(str(i) + '\n')

f.close()
