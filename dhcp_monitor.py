"""
This program monitors the DHCP lease file for changes. Once a change is found, a routine is run to compare the old
leases with the current lease file to send a notifying email with the diff

"""

import sys, os, time
from stat import *
import subprocess
from email_config import Emailconfig
import re

# list used to store new lease values
diff_lease = []
subject_list = []  # use to store body string in list values

with open("leases.txt", "r") as lease_file:
    no_send = lease_file.read().replace('\n', ' ')

# some variables for the eamil from and recipients

send_notification = Emailconfig()


# function to compare the two lease lists
def compare_lists(newlist, oldlist):

    for i in newlist:
        if not re.search(i[-8:].strip(), oldlist):
            print(i[-8:].strip())
            if re.search(i[-8:].strip(), no_send):
                diff_lease.append(i + " soon to go away")
                print(diff_lease[0])
            else:
                diff_lease.append(i)


# function to build the text body of the email from new leases and full list.
# used a list to build the string because strings are immutable so list more efficient
def build_email_body(diff_list, full_list):
    subject_list.append("New leases are: \n ")  # header
    for i in diff_list:
        subject_list.append(i)
    # used to create the full list of values
    subject_list.append(" \n Full List of Leases: \n")  # header
    for i in full_list:
        subject_list.append(i)

    subject_list.append("\n Total Records: " + str(len(current_values)))  # footer with record num count


filename = "/Users/paulmahon/PycharmProjects/ddmon/email_host_list.txt"
# file to monitor for changes
check_file = "/var/lib/dhcp/dhcpd.leases"

# get the current time of the file an save it to a variable (file_time)
file_info = os.stat(check_file)
file_time = file_info[ST_MTIME]

# run a continuous loop to check the file
while True:
    time.sleep(0.2)
    file_info = os.stat(check_file)
    if file_time != file_info[ST_MTIME]:
        file_time = file_info[ST_MTIME]
        # subprocess.call("/root/ddmon/runpython.sh")

        attachment = open(filename, "r")
        current_values = attachment.readlines()
        attachment.close()

        oldvalues = open("/Users/paulmahon/PycharmProjects/ddmon/saved_values.txt", 'r')
        save_values = oldvalues.read().replace('\n',' ')
        oldvalues.close()

        # compare both files ---if the same --- end program ( mo new leases)
        compare_lists(current_values, save_values)

        tosaverecords = open("/Users/paulmahon/PycharmProjects/ddmon/saved_values.txt", "w")
        for i in current_values:
            tosaverecords.write(i)
        tosaverecords.close()
        print("hello")

        if len(diff_lease) != 0:
            
            build_email_body(diff_lease, current_values)

            diff_lease.clear()
            body_string = " ".join(subject_list)  # this will be the body of the email
            subject_list.clear()

            send_notification.send_email(body_string)  # using email class instead

            time.sleep(0.2)
