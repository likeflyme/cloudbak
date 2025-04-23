import pyotp

base = pyotp.random_base32()

print(base)
# 生成一个 TOTP 秘钥
totp = pyotp.TOTP(base)
secret = totp.secret
print(secret)

# 生成 QR 码
uri = totp.provisioning_uri(name="example@domain.com", issuer_name="My Website")
print(uri)

ntotp = pyotp.TOTP(secret)

nuri = ntotp.provisioning_uri(name="example@domain.com", issuer_name="My Website")
print(nuri)
