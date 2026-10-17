import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Verizon Gateways
# SMS: number@vtext.com (Short text)
# MMS: number@vzwpix.com (Long text + Pictures)
VERIZON_MMS = "7579150229@vzwpix.com"
USER_EMAIL = "danielausgtin70172@gmail.com"

# Recipients List
ALERT_LIST = [VERIZON_MMS, USER_EMAIL]

def send_alert(subject, body, attachment_path=None):
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD") # App Password

    if not sender_email or not sender_password:
        print("⚠️ Alert Skipped: EMAIL_SENDER and EMAIL_PASSWORD needed in .env")
        return False

    success_count = 0
    
    # Setup Server once (efficient)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        for recipient in ALERT_LIST:
            try:
                msg = MIMEMultipart()
                msg['From'] = "Midas AI"
                msg['To'] = recipient
                msg['Subject'] = subject
                
                # Attach Body
                msg.attach(MIMEText(body, 'plain'))
                
                # Attach File (Image or Audio)
                if attachment_path and os.path.exists(attachment_path):
                    from email.mime.base import MIMEBase
                    from email import encoders
                    import mimetypes
                    
                    ctype, encoding = mimetypes.guess_type(attachment_path)
                    if ctype is None or encoding is not None:
                        # No guess could be made, or the file is encoded (compressed), so
                        # use a generic bag-of-bits type.
                        ctype = 'application/octet-stream'
                        
                    maintype, subtype = ctype.split('/', 1)
                    
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase(maintype, subtype)
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment_path)}",
                    )
                    msg.attach(part)

                text = msg.as_string()
                server.sendmail(sender_email, recipient, text)
                print(f"📱 Alert sent to {recipient}")
                success_count += 1
                
            except Exception as inner_e:
                print(f"Failed to send to {recipient}: {inner_e}")

        server.quit()
        return success_count > 0
        
    except Exception as e:
        print(f"Failed to connect to SMTP server: {e}")
        return False

if __name__ == "__main__":
    # Test
    print("Testing Alert System...")
    send_alert("Midas Test", "This is a test alert from your AI trading assistant.")
