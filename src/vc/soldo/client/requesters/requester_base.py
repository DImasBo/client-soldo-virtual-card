import logging
import requests

from vc import settings
from vc.libs.decoratos import response_builder
from vc.soldo.client.requesters.schema_base import HeadersSoldoBase, HeadersSoldo, JWTData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequesterSoldoBase(object):
    url: str = settings.API_URL
    default_authorize = HeadersSoldoBase
    advanced_authorize = HeadersSoldo
    auth2_data: JWTData

    @response_builder(data_schema=JWTData)
    def oauth_authorize(self, client_id: str = settings.CLIENT_ID, client_secret: str = settings.CLIENT_SECRET):
        api_path = f'/oauth/authorize'
        print(client_id, client_secret)
        response_data = self.request(
            self.url + api_path, method='post',
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"client_id":client_id, "client_secret": client_secret})
        return response_data

    def request(
            self, url: str, method: str = "get", *,
            headers: dict = None,
            params: str = None, data: dict = None,
            json: dict = None,
            **kwargs):
        print(url, method, headers, params, data, json)

        r = requests.request(url=url, method=method, headers=headers, json=json, data=data, params=params, **kwargs)
        print(r.text)
        if r.status_code == 401 and "invalid_token" in r.text:
            response_data = self.oauth_authorize()
            settings.ACCESS_TOKEN = response_data.data.access_token
            return self.request(url, method,  headers=self.default_authorize().dict(),
                                params=params, data=data, json=json)

        data = r.text
        try:
            data = r.json()
        except:
            pass
        finally:
            # fix long response
            if isinstance(data, str):
                data = data[:400]
        return data, r.status_code, r.url
