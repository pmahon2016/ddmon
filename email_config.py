import smtplib


class Emailconfig():

    def __init__(self):
        self.fromaddr = 'username@gmail.com'  # your from address @gmail.com
        self.toaddr = 'anyaddress@anyname.com'  # to address
        self.email_pass = 'enterpassword'  # password
        self.elogin = 'username'  # your login ID typically w/o @gmail.com

    def send_email(self, btext):

        # update your settings for your google mail (gmail)  account here

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.elogin, self.email_pass)
            server.sendmail(self.fromaddr, self.toaddr, btext)
            server.close()
            print("email sent successfully")
        except:
            print("Your email was not sent")
