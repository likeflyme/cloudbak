from enum import StrEnum


class ClientType(StrEnum):
    WINDOWS = 'win'
    MACOS = 'mac'


class WindowsVersion(StrEnum):
    V3 = 'v3'
    V4 = 'v4'
