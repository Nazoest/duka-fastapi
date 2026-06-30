import cloudinary
import cloudinary.uploader
from send_email import send_email
CLOUDINARY_URL = "dv2xhb0ka"
API_KEY = "796981219386665"
API_SECRET = "fcDMg3dQSbKN6q9OsLJp19hu1KI"

cloudinary.config(
    cloud_name=CLOUDINARY_URL,
    api_key=API_KEY,
    api_secret=API_SECRET
)


def upload_pdf(pdf_file):
    res = cloudinary.uploader.upload(f"receipts/{pdf_file}.pdf", resource_type="raw")
    print(res["secure_url"])
    send_email("nathanmacharia115@gmail.com", "Payment Receipt", f"Thank you for buying from DukaFastAPI. Your receipt is available at: {res['secure_url']}")
    return "success"


#print(upload_pdf("UDREY2AQLN"))