import os

from email.message import EmailMessage

class BaseEmail:
    SUBJECT = ""
    BODY_TEMPLATE = ""
    ATTACHMENTS = {}  # kwarg -> filename mapping

    def __init__(self, sender, recipient, **kwargs):
        self.sender = sender
        self.recipient = recipient
        self.kwargs = kwargs or {}

        self.msg = EmailMessage()

    def add_attachment(self, path, filename=None):
        with open(path, "rb") as f:
            self.msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=filename or os.path.basename(path),
            )

    def build(self):
        self.msg["From"] = self.sender
        self.msg["To"] = self.recipient
        self.msg["Subject"] = self.SUBJECT.format(**self.kwargs)
        self.msg.set_content(self.BODY_TEMPLATE.format(**self.kwargs))

        for key, filename in self.ATTACHMENTS.items():
            if key in self.kwargs:
                self.add_attachment(self.kwargs[key], filename)

        return self.msg
