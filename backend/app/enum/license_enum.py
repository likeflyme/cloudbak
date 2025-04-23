from enum import IntEnum


class EncryptMethod(IntEnum):
    AES = 0
    RSA = 1


class LicenseType(IntEnum):
    NONE = 0
    PRO = 1
    ENTERPRISE = 2

