import requests
import json
from qkd import *
import numpy
import random
import numpy

def test(rx_qubits, rx_basis):
  random.seed()
  key = '404c368bf890dd10abc3f4209437fcbb'
  # Multiply the amount of bits in the encryption key by 4 to obtain the amount of basis.
  sat_basis = [random.choice('+x') for _ in range(len(key)*16)]
  measured_bits = measure(unmarshal(rx_qubits), sat_basis)
  binary_key, err = compare_bases_and_generate_key(rx_basis, sat_basis, measured_bits)
  if err:
    return None, None, err
  # ENCRYPTION_KEY is in hex, so multiply by 4 to get the bit length.
  binary_key = binary_key[:len(key)*4]
  if len(binary_key) < (len(key)*4):
    return None, sat_basis, "not enough bits to create shared key: %d want: %d" % (len(binary_key), len(key))
  return binary_key, sat_basis, None


def validate(q):
    p0 = round(pow(q.real, 2), 1)
    p1 = round(pow(q.imag, 2), 1)
    random.seed()

    try:
        numpy.random.choice(numpy.arange(0, 2), p=[p0, p1])
    except ValueError:
        return False
    return True

def find_prob(total, step=0.1, rotate=False):
    rx = []
    i = 0.0
    while i <= 1 and len(rx) < total:
        j = 0.0
        while j <= 1 and len(rx) < total:
            qx = {'real': round(i, 2), 'imag': round(j, 2)}
            q = complex(qx['real'], qx['imag'])

            if rotate:
                qr = rotate_45(q)
                if validate(qr):
                    rx.append({"real": qx['real'], "imag": qx['imag']})
            else:
                if validate(q):
                    rx.append({"real": qx['real'], "imag": qx['imag']})
            j += step
        i += step
    return rx

def random_qubits():
    qubits = []
    _x = find_prob(512, 0.2, True)
    _r = find_prob(512, 0.2, False)
    basis = [random.choice('+x') for _ in range(512)]
    qubits = []

    for b in basis:
        if b == '+':
            qubits.append(random.choice(_r))
        else:
            qubits.append(random.choice(_x))

    data = {
        "basis": basis,
        "qubits": qubits
        }

def post(data):
    headers = {
            "Content-Type": "application/json",
            }

    rsp = requests.post(
            'https://cryptoqkd.web.ctfcompetition.com/qkd/qubits',
            data=json.dumps(data),
            headers=headers)

    print(rsp.text)
    sat = rsp.json()
    print(sat["basis"]==data["basis"])
    ann = int(sat["announcement"], 16)
    print(ann)
    """
    the encryption key should be 16bytes = 128bits long, guess announce XOR the shared key to get the encryption key
    """
    print(hex(ann^(2**128-1)))

#random.seed()
basis = ['+'] * 512
qubits = [{'real': 0, 'imag': 1}]*512
data = {
        "basis": basis,
        "qubits": qubits
        }
post(data)
