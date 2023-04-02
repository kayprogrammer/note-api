from rest_framework.response import Response


class CustomSuccessResponse(Response):
    def __init__(self, data, status=200, **kwargs):
        resp = {"status": "success"}
        resp.update(data)
        super().__init__(data=resp, status=status, **kwargs)


class CustomErrorResponse(Response):
    def __init__(self, data, status=400, **kwargs):
        resp = {"status": "failure"}
        resp.update(data)
        super().__init__(data=resp, status=status, **kwargs)
