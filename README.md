https://youtu.be/6lqt3ZQwHfg

# DHCP and DNS setup and Monitoring Tool for Raspberry PI
- Use your Raspberry PI (RPI) to take control of your DNS and DHCP requests
- Get email alerts as devices join your network. Monitor DNS access to see DNS queries per each device request. 
- Enjoy faster DNS query response time with your own DNS caching server

                                                  Wireless Access Point (AP)     
            |Raspberry PI| ---ethernet----> |Fios/Cable/DSL WIFI Router|
             192.168.1.10                         192.168.1.1
                eth0     
                    ^  DHCP
                    |  DNS
                    |           
                    |           
          WIFI Clients (from DHCP)
            192.168.1.x
            255.255.255.0
            DNS 192.168.1.10
            Gateway: 192.168.1.1
                               
*If you want or need to use different IPs (ex. 10.0.0.x) do a find and replace in the ddmon directory of your RPI

*disable DHCP on your home router/AP

*make sure the ethernet cable is connected from the RPI to the AP/router  (this is required for eth0 to load for DHCP service)

     Step 1: clone this repo to the root home dir of your RPI (/root/git clone https://github.com/pmahon2016/ddmon.git )
     Step 2: to install apps and services type -> /root/ddmon/install.sh
   ####                       THE RPI WILL REBOOT !!!!                
    
     Step 3: login with ssh to 192.168.1.10 to confgure your gmail account
                      -Please be sure to setup an gmail mail account to use for alerts
                      -Edit the /root/ddmon/email_config.py file to enter your google account information
                      -Configure app security on gmail -> https://myaccount.google.com/lesssecureapps?pli=1
     
     Step 4: Run the following services: 
                      -systemctl start bind9   ( DNS Server)
                      -systemctl start isc-dhcp-server
                      -systemctl start lease_renew.service
                      
   ### Finally: Make sure that the key services are running to confirm operation of your new DHCP and DNS server
   systemctl status bind9  ( confirms DNS)
   systemctl status isc-dhcp-server ( can give errors but start again and look in /var/log/syslog for cause) 
   systemctl status lease_renew.service ( monitoring service - for alerts on new DHCP leases)
                
   As devices get new leases from your DHCP, you should receive alerts from your gmail accoun            
   After some activity,type -> python3 /ddmon/parsequeries.py  ( should generate a report on DNS requests)
   Check /var/log/syslog for errors if something doesn't work or, create an issue here          
              
      ****this is a work-in-progress so leave your comments/Issues 
      
      Thanks!
