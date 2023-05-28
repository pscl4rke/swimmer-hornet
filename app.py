

import datetime
from urllib.parse import urlparse, parse_qs
from wsgiref.simple_server import make_server  # , demo_app


COUNTERS = {"main": 0}


def get_dates(before=None):
    if before is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(before, "%Y-%m-%d").date()
    print("Getting for", date)
    for i in range(50):
        date = date - datetime.timedelta(days=1)
        yield date.strftime("%Y-%m-%d")


def main_app(environ, start_response):
    if environ["PATH_INFO"] == "/":
        with open("page.html", "rb") as srcfile:
            content = srcfile.read()
        start_response("200 OK", [("Content-type", "text/html")])
        return [content]
    elif environ["PATH_INFO"] == "/counter":
        start_response("200 OK", [("Content-type", "text/html")])
        COUNTERS["main"] += 1
        return [f"Seen <b>{COUNTERS['main']}</b> so far".encode()]
    elif environ["PATH_INFO"] == "/days":
        qs = parse_qs(environ["QUERY_STRING"])
        dates = list(get_dates(qs.get("before", [None])[-1]))
        start_response("200 OK", [("Content-type", "text/html")])
        chunks = [f"<h3>Consider {date}</h3>\n".encode() for date in dates]
        chunks.append(f"""<div id="more-{dates[-1]}" hx-get="/days?before={dates[-1]}" hx-swap="outerHTML" hx-trigger="revealed" >Loading...</div>""".encode())
        return chunks
    else:
        start_response("404 Not Found", [("Content-type", "text/html")])
        return [b"<h1>404 Not Found</h1>"]


def main():
    with make_server("127.0.0.1", 8000, main_app) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
