# This program is designed to pull data from the DNS querylog from bind9 to get the hi hits for domain requests
# list the more frequented domains for each user on the network
import re
import time
from operator import itemgetter
from collections import Counter
from socket import gethostbyaddr

start = (time.time())  # track the execution of this module

def get_domain_list():
    search_pattern = re.compile(r'query:\s(.*?)\s')
    domain_list = re.findall(search_pattern,query_log)
    temp = Counter(domain_list)
    top_list = sorted(temp.items(), key=itemgetter(1), reverse=True)
    for i in range(0,20):
        print("{:<40} {}".format(top_list[i][0],top_list[i][1]))

# function to parse the dhcp lease file for host names if not resolved by getaddr
def get_name_dhcp(ip):
    s = dhcpleases.split(ip)[-1]
    s = s.split('}')[0]
    p = r'client-hostname(.+?);'
    match = (re.search(p, ascii(s)))
    if match:
        return match.group(1)[2:-1]
    return "No Name"


# routine to map the ips to domain name
def get_name_dns(ip):
    try:
        host = gethostbyaddr(ip)
        return host[0]
    except:
        return get_name_dhcp(ip)  # try to pull the hostname from the dhcp lease file


def open_file(filename):
    with open(filename, 'r') as of:
        ret_object = of.read()
        return ret_object

# Open the files for processing
dhcpleases = open_file('/var/lib/dhcp/dhcpd.leases')
query_log = open_file('/var/cache/bind/querylog')


def get_ip_activity():
    p1 = re.compile(r" 192\.168\.1\.\d{1,3}")  # pattern search for IP addresses in up coming loop
    # this is the routine to get the new source IPs
    query_list = re.findall(p1, query_log)
    # run the counter ot get instances of IPs domain request.
    query_dic = Counter(query_list)  # make a dict with the ip as keys and count of each request as the value
    finallist = sorted(query_dic.items(), key=itemgetter(1), reverse=True)  # provides a sorted list


    print("Top 20 List \t \t \t  Hits")
    for i in range(0, 20):
        if finallist[i]:
            print("IP:{} \t {:>10} \t {:>10}".format(finallist[i][0], finallist[i][1], get_name_dns(finallist[i][0][1:])))

    finish = time.time()
    print("\nTime to run this program:  {}\n".format(finish - start))


if __name__ == '__main__':
    get_ip_activity()
    get_domain_list()

