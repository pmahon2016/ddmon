# DHCP and DNS setup and Monitoring Tool for Raspberry PI
- Use your Raspberry PI (RPI) to take control of your DNS and DHCP requests
- Receive email notifications when devices join your network. Monitor DNS access to see DNS queries per each device on your       network. 
- Enjoy faster DNS query responses with your own DNS caching server
 

                                                  Wireless Access Point (AP)     
            |Raspberry PI| ---ethernet----> |Fios/Cable/DSL WIFI Router|
             192.168.1.10                         192.168.1.1
                eth0      ^\
                             \ DHCP
                              \ DNS
                               \
                               
                             WIFI Clients (from DHCP)
                               192.168.1.x
                               255.255.255.0
                               DNS 192.168.1.10
                               Gateway: 192.168.1.1
                               
*If you want or need to use different IPs (ex. 10.0.0.x) do a find and replace in the ddmon directory of your RPI

*disable DHCP on your home router/AP

*make sure the ethernet cable is connected from the RPI to the AP/router  (this is required for eth0 to load for DHCP service)

     Step 1: clone this repo to the root home dir of your RPI (/root/git clone https://github.com/pmahon2016/ddmon.git )
     Step 2: set script permission on install.sh   (/root/ddmon/chmod u+x install.sh)
     Step 3: to install apps and services type -> /root/ddmon/install.sh
     Step 4: to load DHCP & DNS type:
                     -systemctl start bind9
                     -systemctl start isc-dhcp-server
                     -if both start without any issue type -> systemctl restart bind9  (required to take log settings)
                     
     Step 5: Confgure gmail account and turn on DHCP monitoring tool. 
                      -Edit /root/ddmon/email_config.py file to enter your google account information
                      -Please be sure to setup an gmail mail account 
                      -Configure app security on gmail -> https://myaccount.google.com/lesssecureapps?pli=1
                      -Run the monitor file       -> python3 /root/ddmon/dhcp_monitor.py (loads the DHCP monitoring file. as n 
                       device requests are generated, you should receive an email notification )
                      -After some activity,type -> python3 /ddmon/parsequeries.py  ( should generate a report on DNS requests)
     
     Step 6: Run the DHCP monitoring tool as a service/process
                      -systemctl start lease_renew.service     
                 
      ****this is a work-in-progress so leave your comments/Issues 
      
      Thanks!
