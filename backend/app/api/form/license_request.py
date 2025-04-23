from pydantic import BaseModel


class LicenseRequest(BaseModel):
    license_text: str