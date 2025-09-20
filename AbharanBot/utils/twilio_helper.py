from flask import Response
from twilio.twiml.messaging_response import MessagingResponse

def send_message(text, options=None):
    resp = MessagingResponse()
    msg = resp.message(text)

    if options:
        # Use WhatsApp quick reply (interactive buttons not available in Twilio free sandbox)
        menu_text = "\n".join([f"- {opt}" for opt in options])
        msg.body(f"{text}\n\nOptions:\n{menu_text}")

    return Response(str(resp), mimetype="application/xml")
