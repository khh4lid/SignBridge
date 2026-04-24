from pyezviz import EzvizClient, EzvizCamera
import requests

EMAIL = "khaled0wleed@gmail.com"
PASSWORD = "0500131217Kk"
SERIAL = "L06480056"

client = EzvizClient(EMAIL, PASSWORD, "apiisgp.ezvizlife.com")
client.login()
print("✅ تم الدخول!")

cam = EzvizCamera(client, SERIAL)
status = cam.status()

# جيب آخر صورة
pic = status.get('last_alarm_pic')
print(f"🖼️ رابط الصورة: {pic}")

if pic:
    img = requests.get(pic)
    with open('/home/khaled/test_pic.jpg', 'wb') as f:
        f.write(img.content)
    print("✅ تم حفظ الصورة: test_pic.jpg")
