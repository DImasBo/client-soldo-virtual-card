from vc.soldo.client.requesters.schema_base import ResponseData

class ClientException(Exception):

    def __init__(self, status_code, msg:str ):
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return f"{self.status_code}, {self.msg}"

    # def to_dict(self):
        # return dict(loc=["amount"], msg=self.msg, type=)


def response_builder(expected_code=200, response_schema=ResponseData, data_schema=None):
    def wrapper(func):
        def builder(*args, **kwargs):
            data, status_code, url = func(*args, **kwargs)
            print(data)
            response = response_schema(status_code=status_code, url=url, **data)
            if status_code == expected_code:
                if data_schema:
                    try:
                        if isinstance(data, list):
                            response.data = data
                        else:
                            response.data = data_schema(**data)
                    except Exception as e:
                        print(data)
                        raise e
            return response

        return builder

    return wrapper