from django.core.mail.backends.base import BaseEmailBackend
import resend
import os

class ResendEmailBackend(BaseEmailBackend):
    def open(self):
        resend.api_key = os.environ.get('RESEND_API_KEY')

    def close(self):
        pass

    def send_messages(self, email_messages):
        resend.api_key = os.environ.get('RESEND_API_KEY')
        sent = 0
        for message in email_messages:
            try:
                body = message.body
                html = None
                for content, mimetype in getattr(message, 'alternatives', []):
                    if mimetype == 'text/html':
                        html = content
                        break

                params = {
                    "from": message.from_email,
                    "to": message.to,
                    "subject": message.subject,
                    "text": body,
                }
                if html:
                    params["html"] = html

                resend.Emails.send(params)
                sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise
        return sent