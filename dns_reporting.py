# This program is designed to pull data from the DNS querylog from bind9 to get the hi hits for domain requests
# list the more frequented domains for each user on the network
import re
import time
from operator import itemgetter
from collections import Counter
from socket import gethostbyaddr

start = (time.time())  # track the execution of this module


# used for various printing - this is a generator to print the first N lines
def printing_station(dic_object, count):
    counter = 0
    for k, v in dic_object.items():
        if counter == count:
            return
        counter += 1
        yield "{:<50} {}".format(str(k), str(v))


def get_domain_list():
    search_pattern = re.compile(r'query:\s(.*?)\s')
    domain_list = [re.search(search_pattern, x).group() for x in query_log]
    temp = Counter(domain_list)
    top_list = dict(sorted(temp.items(), key=itemgetter(1), reverse=True))  # Sort the list and return a dictionary
    [top_list.pop(y) for x in white_list for y in top_list.copy() if re.search(x, str(y))]  # filter out certain safe domains
    print(len(top_list))
    for items in printing_station(top_list, 20):  # call the printing generator
        print(items)


# function to parse the dhcp lease file for host names if not resolved by getaddr
def get_name_dhcp(ip):
    s = [x.split(ip)[-1] for x in dhcpleases]
    s = [x.split('}')[0] for x in s]
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
        ret_object = of.readlines()
        return ret_object


# Open the files for processing
dhcpleases = open_file('/var/lib/dhcp/dhcpd.leases')
query_log = open_file('/var/cache/bind/querylog')
white_list = open_file('white_list.txt')


def get_ip_activity():
    p1 = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")  # pattern search for IP addresses in up coming loop
    # this is the routine to get the new source IPs
    query_list = [re.search(p1, x).group() for x in query_log]
    # run the counter ot get instances of IPs domain request.
    query_dic = Counter(query_list)  # make a dict with the ip as keys and count of each request as the value
    finallist = dict(sorted(query_dic.items(), key=itemgetter(1), reverse=True))  # provides a sorted list

    print("Top 20 List \t \t \t  Hits")
    for items in printing_station(finallist, 20):
        print("{:<70} {}".format(items, get_name_dns(items[:15:].strip())))

    print("\n")


if __name__ == '__main__':
    get_ip_activity()
    get_domain_list()

finish = time.time()
print("\nTime to execute:  {}\n".format(finish - start))