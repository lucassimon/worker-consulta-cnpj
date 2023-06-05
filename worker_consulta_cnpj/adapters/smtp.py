import smtplib


class SmtpLibAdapter:

    def __init__(self, port, host) -> None:
        self.port = port
        self.host = host

    def send(self, msg):
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.sendmail(msg['from'], msg['to'], msg.as_string())
        except Exception as err:
            raise err
