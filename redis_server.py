import redis
from aiohttp import web

def get_client():
    client = redis.Redis(decode_responses=True)
    return client


async def request_add(request: web.Request):
    text = await request.json()
    sent = text.get("sent", "")
    weight = text.get("weight", "")
    for i in range(len(sent)):
        key = 'http_autocomplete:' + sent[:i + 1]
        print(key)
        get_client().zincrby(key, weight, sent)
    return web.Response(text="success")


async def request_query(request: web.Request):
    text = await request.json()
    word = text.get("word", "")
    key = 'http_autocomplete:' + word
    sent_list = get_client().zrevrange(key, 0, -1)
    print("key: {}, ret: {}".format(key, sent_list))
    return web.json_response(data={"sent_list": sent_list})


class Application(web.Application):
    def __init__(self):
        super().__init__()
        self.add_routes()

    def add_routes(self):
        self.router.add_route("post", "/add", request_add)
        self.router.add_route("post", "/query", request_query)

    def run_app(self):
        web.run_app(self, port=8000)


if __name__ == '__main__':
    application = Application()
    application.run_app()
