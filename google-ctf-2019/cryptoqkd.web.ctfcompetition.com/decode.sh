key="404c368bf890dd10abc3f4209437fcbb"
ciphertext="U2FsdGVkX182ynnLNxv9RdNdB44BtwkjHJpTcsWU+NFj2RfQIOpHKYk1RX5i+jKO"

key="946cff6c9d9efed002233a6a6c7b83b1"
ciphertext="U2FsdGVkX19OI2T2J9zJbjMrmI0YSTS+zJ7fnxu1YcGftgkeyVMMwa+NNMG6fGgjROM/hUvvUxUGhctU8fqH4titwti7HbwNMxFxfIR+lR4="

echo "$key" > /tmp/plain.key; xxd -r -p /tmp/plain.key > /tmp/enc.key
echo "$ciphertext" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key
