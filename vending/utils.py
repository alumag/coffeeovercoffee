import serial

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

    return "".join([hex(value)[2:] for value in lst[::-1]])


def write_packet(encrypted_hex):
    """ Send the data to the arduino """
    s = serial.Serial("/dev/ttyUSB0", 115200)
    s.write(bytearray.fromhex(encrypted_hex))
    s.close()
