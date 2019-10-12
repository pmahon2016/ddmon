class Emailconfig():

# should not be replicated

    def send_email(self, btext):
        import smtplib

        # update your settings for your google mail (gmail)  account here
        fromaddr = 'username@gmail.com'  # your from address @gmail.com
        toaddr = 'anyaddress@anyname.com'  # to address
        email_pass = 'enterpassword'  # password
        elogin = 'username'  # your login ID typically w/o @gmail.com

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(elogin, email_pass)
            server.sendmail(fromaddr, toaddr, btext)
            server.close()
            print("email sent successfully")
        except:
            print("Your email was not sent")
