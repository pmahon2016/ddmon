# DHCP and DNS setup and Monitoring Tool for Raspberry PI
- Use your Raspberry PI (RPI) to take control of your DNS and DHCP requests
- Receive email notifications when devices join your network. Monitor DNS access to see DNS queries per each device on your       network. 
- Enjoy faster DNS query responses with your own DNS caching server
 

                                                            
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

     Step 1: clone this repo to the root home dir of your Raspberry Pi
     Step 2: from the /root/ddmon dir...type ./install.sh
     Step 3: to load DHCP & DNS type:
                     systemctl start bind9
                     systemctl start isc-dhcp-server
     Step 4: Confgure gmail account and turn on DHCP monitoring tool. 
                      Edit /root/ddmon/email_config.py file to enter your google account information
                      Please be sure to setup an gmail mail account 
                      configure app security on gmail -> https://myaccount.google.com/lesssecureapps?pli=1
                      run the monitor file -> /root/ddmon/python3 dhcp_monitor.py
     
      ****this is a work-in-progress so leave your comments/Issues 
      
      Thanks!
