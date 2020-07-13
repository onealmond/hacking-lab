import random
import numpy

from math import sqrt
#from flask import current_app

def rotate_45(qubit):
  return qubit * complex(0.707, -0.707)

def measure(rx_qubits, basis):
  measured_bits = ""
  for q, b in zip(rx_qubits, basis):
    if b == 'x':
      q = rotate_45(q)
    probability_zero = round(pow(q.real, 2), 1)
    probability_one = round(pow(q.imag, 2), 1)
    #print('validate', b, q, probability_zero, probability_one, probability_zero+probability_one)
    measured_bits += str(numpy.random.choice(numpy.arange(0, 2), p=[probability_zero, probability_one]))
  return measured_bits

def compare_bases_and_generate_key(tx_bases, rx_bases, measure):
  """Compares TX and RX bases and return the selected bits."""
  if not (len(tx_bases) == len(rx_bases) == len(measure)):
    return None, "tx_bases(%d), rx_bases(%d) and measure(%d) must have the same length." % (len(tx_bases), len(rx_bases), len(measure))
  ret = ''
  for bit, tx_base, rx_base in zip(measure, tx_bases, rx_bases):
    if tx_base == rx_base:
      ret += bit
  return ret, None

def unmarshal(qubits):
  return [complex(q['real'], q['imag']) for q in qubits]

# Receive user's qubits and basis, return the derived key and our basis.
def perform(rx_qubits, rx_basis):
  random.seed()
  # Multiply the amount of bits in the encryption key by 4 to obtain the amount of basis.
  sat_basis = [random.choice('+x') for _ in range(len(current_app.config['ENCRYPTION_KEY'])*16)]
  measured_bits = measure(unmarshal(rx_qubits), sat_basis)
  binary_key, err = compare_bases_and_generate_key(rx_basis, sat_basis, measured_bits)
  if err:
    return None, None, err
  # ENCRYPTION_KEY is in hex, so multiply by 4 to get the bit length.
  binary_key = binary_key[:len(current_app.config['ENCRYPTION_KEY'])*4]
  if len(binary_key) < (len(current_app.config['ENCRYPTION_KEY'])*4):
    return None, sat_basis, "not enough bits to create shared key: %d want: %d" % (len(binary_key), len(current_app.config['ENCRYPTION_KEY']))
  return binary_key, sat_basis, None
