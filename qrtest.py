import qrcode
import base64

qris_code = "https://example.com/payment?transaction_id=123456"

qris_b64 = base64.urlsafe_b64encode(qris_code.encode()).decode()
qris_url = f"https://ki-ar-kod.netlify.app/?data={qris_b64}"

print(f"Buka link berikut untuk melihat QRIS:\n{qris_url}")