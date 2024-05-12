from falcon import Request, Response, HTTP_200


class TestRender:
    route = '/render'

    def on_get(self, req: Request, resp: Response) -> None:
        resp.content_type = 'text/html'
        resp.status = HTTP_200
        resp.body = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Test Button</title>
                <style>
                    .btn {
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                    }
                    .btn:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <button class="btn">Click Me</button>
            </body>
            </html>
        """
