import timeit

my_number = 1000
my_starter = """

import re
from operator import itemgetter
from collections import Counter

"""

my_code = """ 
with open('/var/cache/bind/querylog', 'r') as query_logfile:
    query_log = query_logfile.readlines()

    # query_list = []  # put all the values and and run a counter to get the number of instances for each domain
    p1 = re.compile(\'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\')  # pattern search for IP addresses in up coming loop
    # this is the routine to get the new source IPs
    query_list = [re.search(p1, i).group() for i in query_log]

    # run the counter ot get instances of IPs domain request.
    query_dic = Counter(query_list)  # make a dict with the ip as keys and count of each request as the value
    finallist = sorted(query_dic.items(), key=itemgetter(1), reverse=True)  # provides a sorted list



"""

result = timeit.timeit(stmt=my_code,setup=my_starter,number=my_number)

print(result/my_number)