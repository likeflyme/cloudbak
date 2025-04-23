from app.helper.licence import LicenseManager
from app.services.sys_conf_service import get_sys_info


def get_sys_license():
    sys_info = get_sys_info()
    if sys_info.license:
        return LicenseManager.parse_license(sys_info.license)
    return None
