from pyezviz import EzvizClient, EzvizCamera
from pyezviz.constants import DeviceSwitchType

EMAIL = "khaled0wleed@gmail.com"
PASSWORD = "0500131217Kk"
SERIAL = "L06480056"

client = EzvizClient(EMAIL, PASSWORD, "apiisgp.ezvizlife.com")
client.login()
cam = EzvizCamera(client, SERIAL)

# شوف كل السويتشات المتاحة
print("📋 السويتشات:")
for s in DeviceSwitchType:
    print(f"  - {s.name} = {s.value}")
