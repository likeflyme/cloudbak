import hashlib
import hmac
import struct
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


IV_SIZE = 16
HMAC_SHA256_SIZE = 64
KEY_SIZE = 32
AES_BLOCK_SIZE = 16
ROUND_COUNT = 256000
PAGE_SIZE = 4096
SALT_SIZE = 16
SQLITE_HEADER = b"SQLite format 3"


def decrypt_db_file_v4(path: str, pkey: str, output_path: str):
    """
    Decrypts the SQLite database file and writes the result to the specified output file.
    """
    with open(path, 'rb') as f:
        buf = f.read()

    # If the file starts with SQLITE_HEADER, no decryption is needed
    if buf.startswith(SQLITE_HEADER):
        with open(output_path, 'wb') as out_file:
            out_file.write(buf)
        return

    decrypted_buf = bytearray()

    # Get the salt from the start of the file for key decryption
    salt = buf[:16]
    # XOR salt with 0x3a to get the mac_salt
    mac_salt = bytes(x ^ 0x3a for x in salt)

    # Decode the pkey from hex
    pass_key = bytes.fromhex(pkey)

    # PBKDF2 to derive the decryption key
    key = pbkdf2_hmac(pass_key, salt, ROUND_COUNT)

    # PBKDF2 to derive the mac_key
    mac_key = pbkdf2_hmac(key, mac_salt, 2)

    # Append the SQLite header to the decrypted buffer
    decrypted_buf.extend(SQLITE_HEADER)
    decrypted_buf.append(0x00)

    # Calculate reserve size for hash verification and padding
    reserve = IV_SIZE + HMAC_SHA256_SIZE
    reserve = (reserve + AES_BLOCK_SIZE - 1) // AES_BLOCK_SIZE * AES_BLOCK_SIZE

    total_page = len(buf) // PAGE_SIZE
    for cur_page in range(total_page):
        offset = SALT_SIZE if cur_page == 0 else 0
        start = cur_page * PAGE_SIZE
        end = start + PAGE_SIZE

        # Compute HMAC hash for verification
        hash_mac = compute_hmac(mac_key, buf[start + offset:end - reserve + IV_SIZE], cur_page + 1)

        # Check if hash matches
        hash_mac_start_offset = end - reserve + IV_SIZE
        hash_mac_end_offset = hash_mac_start_offset + len(hash_mac)
        if hash_mac != buf[hash_mac_start_offset:hash_mac_end_offset]:
            raise Exception("Hash verification failed")

        # Decrypt the content using AES-256-CBC
        iv = buf[end - reserve:end - reserve + IV_SIZE]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(buf[start + offset:end - reserve]) + decryptor.finalize()

        decrypted_buf.extend(decrypted_data)
        decrypted_buf.extend(buf[end - reserve:end])

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as out_file:
        out_file.write(bytes(decrypted_buf))


def pbkdf2_hmac(key, salt, iterations):
    """
    Derives a key using PBKDF2-HMAC.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations
    )
    return kdf.derive(key)


def compute_hmac(mac_key, data, page_number):
    """
    Computes the HMAC-SHA512 hash for the given data and page number.
    """
    mac = hmac.new(mac_key, digestmod=hashlib.sha512)  # Use hashlib.sha512 instead of cryptography's SHA512
    mac.update(data)
    mac.update(struct.pack("<I", page_number))  # Add the page number to the hash
    return mac.digest()


# Example usage:
input_path = "C:\\Users\\Administrator\\Desktop\\message_0.db"
key = "b1d0260305f94988af7af8bd5130165fc3a6262d1fa54661b3529161fc48a54a"
output_path = "C:\\Users\\Administrator\\Desktop\\decoded_message_0.db"
decrypt_db_file_v4(input_path, key, output_path)
