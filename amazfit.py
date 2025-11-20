import warnings
warnings.filterwarnings("ignore", category=Warning)
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# ----------------------------
# CONFIG
# ----------------------------
PRODUCT_URL = "https://in.amazfit.com/products/helio-strap"   # Replace with your actual product link
YOUR_EMAIL = os.getenv("EMAIL_USER")
YOUR_APP_PASSWORD = os.getenv("EMAIL_PASS")
SEND_TO = os.getenv("EMAIL_USER")

# ----------------------------
# SEND EMAIL FUNCTION
# ----------------------------
def send_email():
    msg = MIMEText(f"Product is now in stock! Check here: {PRODUCT_URL}")
    msg["Subject"] = "PRODUCT IN STOCK!"
    msg["From"] = YOUR_EMAIL
    msg["To"] = SEND_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, SEND_TO, msg.as_string())

    print("Email sent!")

# ----------------------------
# CHECK STOCK FUNCTION
# ----------------------------
def check_stock():
    page = requests.get(PRODUCT_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")

    button = soup.find("button", {"id": "card-submit-button-template--21880927682596__main"})

    if not button:
        print("Button not found. HTML may have changed.")
        return

    button_text = button.get_text(strip=True)
    is_disabled = button.has_attr("disabled")

    # Conditions for in-stock
    if not is_disabled and button_text.lower() not in ["coming soon"]:
    # if True:
        print("Product is IN STOCK!")
        send_email()
    else:
        print("Still OUT OF STOCK...")

# ----------------------------
# RUN
# ----------------------------
check_stock()
