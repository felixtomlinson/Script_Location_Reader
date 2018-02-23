import smtplib


class Mail(object):
    def __init__(self, username, password):
        self.user = username
        self.password = password

    def login(self):
        server = smtplib.SMTP('smtp.gmail.com', 465)
        server.starttls()
        return server.login(self.user, self.password)
