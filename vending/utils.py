import serial
import time

device = "/dev/ttyUSB0"

def encrypt(blob):
    """ Encrypt coffee packets """
    hex_blob = int(blob, 16)
    lst = list()

    for _ in range(8):
        b = hex_blob & 0xff
        b = b ^ 0xca
        b = b ^ 0xfe
        lst.append(b)
        hex_blob = hex_blob >> 8

    print(lst)
    return lst[::-1]


def write_packet(encrypted_hex):
    """ Send the data to the arduino """
    s = serial.Serial(device, 115200)
    data = serial.to_bytes(encrypted_hex)
    s.write(data)
    print("Write: ", data)
    s.close()

