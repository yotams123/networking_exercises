addr = input("Enter mac address with each byte separated by a colon 'AA:BB:CC:DD:EE:FF' > ")

VALID_CHARS = 'ABCDEF1234567890'
MULTICAST = '13579BDF'

b = addr.split(":")

flag = True if len(b) == 6 else False

for byte in b:
    if len(byte) != 2 or byte[0].upper() not in VALID_CHARS or byte[1].upper() not in VALID_CHARS:
        flag = False

if flag:
    print("Valid MAC address")
    print(f"Vendor ID is {':'.join(b[:3])}")
    if b[0][1] in MULTICAST:
        print("MAC  address is a multicast address")
    else:
        print("MAC address is a unicast address")
else:
    print("Invalid MAC address")
