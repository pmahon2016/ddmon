# This program is designed to pull data from the querylog from bind9 to
# get the hi hits for domain requests
# list the more frequented domains for each user on the network
import re
from operator import itemgetter
from collections import Counter
from socket import gethostbyaddr

# the white list is used to filter out known good domains for reporting
white_list = ['captive.g.aaplimg.com', 'captive-cidr.origin-apple.com.akadns.net',
              'captive-cdn.origin-apple.com.akadns.net', "google.com", 'akamaiedge.net',
              "snapchat.com", "akadns.net", "apple-dns.net", 'in-addr.arpa', 'apple.com'
    , 'cloudfront.net', 'amazon.com', 'spectrum.s3.amazonaws.com', 'wpad.mydomain.com',
              'api.amazonalexa.com', 'ssl.gstatic.com', 'dropbox.com']

newDict = {}  # create dictionary for domains to be added to ip addresses

try:
    domain_list = open('old_domain_list.txt', 'r')
except FileNotFoundError:
    "Please run command again to create file list"
    domain_list = open('old_domain_list.txt', 'w')
    domain_list.close()
    domain_list = open('old_domain_list.txt', 'r')
# convert domain lists to a string

mystring = ''.join(domain_list)

total_domains = []
# this will open the query log file and search through for the data
with open('/var/cache/bind/querylog', "r") as query_logfile:
    query_log = query_logfile.readlines()

    # query_list = []  # put all the values and and run a counter to get the number of instances for each domain
    p1 = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')  # pattern search for IP addresses in upcomign loop
    # this is the routine to get the new source IPs
    query_list = [re.search(p1, i).group() for i in query_log]

    # run the counter ot get instances of IPs domain request.
    query_dic = Counter(query_list)  # make a dict with the ip as keys and count of each request as the value
    finallist = dict(sorted(query_dic.items(), key=itemgetter(1), reverse=True))  # provides a sorted list


    # this routine takes the IP address of each user and finds the associated domain requests
    def search_url(ip_address):
        value_list = []  # a list to hold the full list of the domain requests as keys
        p2 = re.compile(r'query:\s(.*?)\s')  # pattern to search for the domain name
        for i in query_log:
            if ip_address in i:
                s2 = re.search(p2, i)
                domain_name = s2.group(1).split(".")  # split up the string to just get the domain name
                if len(domain_name) > 1:
                    dot = "."
                    domain_only = domain_name[-2:]  # overly complex way to do this but...
                    domain_only = dot.join(domain_only)
                # This routine ensures that known domains names are not included in the list

                if s2 and s2.group(1) not in white_list:  # had to run this separately to catch the full names
                        value_list.append(s2.group(1))  # add the relevent domains to a list
                        total_domains.append(s2.group(1))

        # make dictionary from the value_list with the domains as keys and the number of requests as values.
        tempdict = Counter(value_list)

        for k, v in tempdict.items():
            s3 = re.search(k, mystring)
            if not s3:
                newDict[ip_address].append(str(k) + '99999')

        # sort the list
        temp_list = dict(sorted(tempdict.items(), key=itemgetter(1), reverse=True))

        for k, v in temp_list.items():
            newDict[ip_address].append(str(k) + " " + str(v))  # dict was created earlier - now pop with unique domains


# routine to map the ips to domain name
def nslooky(ip):
    try:
        output = gethostbyaddr(str(ip))
        if output:
            return output[0]
    except:
        output = ip
        return output


# print the heavy hitters on the network and create a new dict with the unique IPs
for k, v in finallist.items():
    # print(nslooky(k) + "\t\t\t" + str(v))
    newDict[k] = []  # create a new dict for ips as keys and the unique domains and instance count as values
    search_url(k)  # send to populate the domains

total_domain_dict = Counter(total_domains)
high_domains = sorted(total_domain_dict.items(), key=itemgetter(1), reverse=True)

print("\t\t Top Ten Requested Domains\n")
for i in range(0, 10):
    if high_domains[i]:
        list_domains = list(high_domains[i])
        print("\t\t " + str(list_domains[0]) + ":" + str(list_domains[1]))

print("\n\n IP Address/Name \t\t\t\t\t\t Domain")
for k, v in newDict.items():
    print(nslooky(k))
    for i in range(0, 5):
        if i < len(v):
            # print(str(k) + "\t\t " + v[i])
            print("\t\t\t\t\t\t\t\t\t {:>10}".format(str(v[i])))

write_domains = open("old_domain_list.txt", "w")
for k, v in newDict.items():
    for i in v:
        write_domains.write(i + "\n")
write_domains.close()
