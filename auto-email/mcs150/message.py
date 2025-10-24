from base_email import BaseEmail

class Message(BaseEmail):
    SUBJECT = "Reminder: MCS-150 Biennial update is due to October!"
    BODY_TEMPLATE = """
Hi {contact_name},

I noticed that {company_name}’s USDOT #{usdot} is due for its MCS-150 biennial update by October 31.
A lot of carriers miss this filing and end up with fines or temporary deactivation, so I wanted to reach out and see if you already have someone handling it.

If not, my team at Truckstop Backoffice can take care of it quickly — no subscriptions or hidden fees.
We can take care of the filing for you for a flat $10 if that would save you the hassle.

Best,
Sergey Shumilov


Truckstop Backoffice
1 East Ave, Rochester, NY 14604  
United States  
+1 (484) 473-2474

If you prefer not to receive future emails from us, reply with the word "UNSUBSCRIBE".
"""
    def build(self):
        super().build()
        if "mcs150_path" in self.kwargs:
            self.add_attachment(self.kwargs["mcs150_path"], "MCS-150 form.pdf")
        if "invoice_path" in self.kwargs:
            self.add_attachment(self.kwargs["invoice_path"], "Invoice.pdf")

        return self.msg
