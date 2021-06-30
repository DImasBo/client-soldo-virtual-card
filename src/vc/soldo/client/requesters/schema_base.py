from typing import TypeVar, Optional

from pydantic.generics import GenericModel, Generic
from .utils import fingerprintHash, fingerprintSignature
from typing import Optional
from pydantic import Extra, BaseModel

from vc import settings


T = TypeVar('T')


class ResponseDataBase(BaseModel):
    pass


class ResponseData(GenericModel, Generic[T]):
    error: Optional[str]
    url: Optional[str]
    status_code: Optional[int]
    error_description: Optional[str]
    message: Optional[str]
    data: Optional[T]


class JWTData(BaseModel):
    refresh_token: str
    token_type: str
    access_token: str
    expires_in: int


class HeadersSoldoBase(BaseModel):
    """
    headers for Standard Authentication
    http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#standard-authentication
    """
    Authorization: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Authorization = f"Bearer {settings.ACCESS_TOKEN}"

    class Config:
        extra = Extra.allow


class HeadersSoldo(HeadersSoldoBase):
    """
    headers for Advanced Authentication
    http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#advanced-authentication
    """
    Content_Type: str = "application/json"
    fingerprintH: Optional[str]
    fingerprintS: Optional[str]

    def __init__(self, data, fields=None, keyPath=settings.PATH_RSA_PRIVATE, **kwargs):
        super().__init__(**kwargs)
        if not fields:
            fields = data.keys()
        fingerprint = ""
        for field in fields:
            if data.get(field):
                fingerprint += str(data.get(field))
                print(fingerprint)
        fingerprint += settings.TOKEN
        print(fingerprint)
        self.fingerprintH = fingerprintHash(fingerprint)
        self.fingerprintS = fingerprintSignature(self.fingerprintH, keyPath)

    class Config:
        fields = {
            "fingerprintS": "X-Soldo-Fingerprint-Signature",
            "fingerprintH": "X-Soldo-Fingerprint",
        }
        extra = Extra.allow
