from falcon import Request, Response, HTTP_200


class TestRender:
    route = '/render'

    def on_get(self, req: Request, resp: Response) -> None:
        resp.status = HTTP_200
        resp.media = {'test': 'render'}
