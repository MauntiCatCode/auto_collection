from mcs150.message import Message
from log import log
from utils import send_email


def send_mcs150_and_invoice(email_from, password, email_to, mcs150_path, invoice_path, dryfire = False, **kwargs) -> None:
    """Sends an email with an MCS-150 form and invoice attached to the specified recipient."""
    log.debug(f"Crafting message for '{email_to}'")
    msg = Message(
        sender = email_from,
        recipient = email_to,
        #mcs150_path = mcs150_path,
        #invoice_path = invoice_path,
        **kwargs
        ).build()
    
    log.debug(f"Sending to '{email_to}'")
    if dryfire:
        log.debug(f"Email fired!")
        return 
    send_email(msg, email_from, password)

