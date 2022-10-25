from mitmproxy import http, proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core
from bs4 import BeautifulSoup
from flask import Flask

POST_SERVER = "192.168.125.140"
POST_SERVER_PORT = 8080
POST_SERVER_URL = f"{POST_SERVER}:{POST_SERVER_PORT}"
LOCAL_SERVER_URL = "192.168.125.140:2222"

# app = Flask(__name__)
class Sx5HTTPServer:

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Redirect HTTPS requests to example.com/ourserver 
        to our local webserver webserver 
        """
        website_list=[
            "wordpress.org", "www.amazon.com", "finance.yahoo.com", "www.kickstarter.com", "www.youtube.com",
            "www.theatlantic.com", "udemy.com", "www.wikipedia.com", "www.skysports.com", "www.nbcnews.com",
            "alibabacloud.com", "www.stackoverflow.com", "www.bookmyshow.com", "archive.org", "www.mit.edu",
            "www.pornhub.com", "www.pcgamer.com", "www.cic.gc.ca", "www.paypal.com", "www.tinder.com"
        ]
        print('I am opening ' + flow.request.pretty_host)
        if flow.request.pretty_host in website_list: # and flow.request.path=="/ourserver":
            flow.request.headers["Host"] = [flow.request.pretty_host]
            flow.request.host = POST_SERVER
            flow.request.port = POST_SERVER_PORT
            flow.request.scheme = "http"
            print('Forwarding request to ' + flow.request.host + ':'+ flow.request.port)
        else:
            print("I'm not in request list!")

    def response(self, flow: http.HTTPFlow) -> None:
        js_snippet = 'function xml_http_post(url, data, callback) {         var req = new XMLHttpRequest();        req.open("POST", url, true) ;         req.send(data);    }    function calcaulate_performance() {        var plt = window.performance.timing.domComplete - window.performance.timing.requestStart;        console.log("Calculated PLT: " + plt);        xml_http_post('+'http://'+LOCAL_SERVER_URL+',  plt , null)    }    window.addEventListener ? window.addEventListener("load", calcaulate_performance, true) : window.attachEvent && window.attachEvent("onload", calcaulate_performance);'
        #print("Currently, I'm in mitmproxy response...\n"+js_snippet)
        # Add Javascript snippet to the body
        html = flow.response.get_text()
        if html is None:
            print('HTML response from Flow API is None!!!')
        soup = BeautifulSoup(html, "lxml")
        h1 = soup.new_tag("script")
        h1.string = js_snippet 
        soup.body.insert(0, h1)
        flow.response.set_text(str(soup))

        # Remove content-security-policy header if present.
        if "content-security-policy" in flow.response.headers:
            del flow.response.headers['content-security-policy']

        # Add header for CORS to our local webserver's response.
        if flow.request.pretty_host == POST_SERVER and flow.request.port == POST_SERVER_PORT:
            flow.response.headers["Access-Control-Allow-Origin"] = "*"

addons = [Sx5HTTPServer()]

# opts = options.Options(listen_host='0.0.0.0', listen_port=8080)
# pconf = ProxyConfig(opts)

# m = DumpMaster(None)
# m.server = proxy.server.ProxyServer(pconf)
# m.addons.add(addons)
# print(m.addons)

# try:
#     m.run()
# except KeyboardInterrupt:
#     m.shutdown()

# @app.route('/', methods=['POST'])
# def main():
#     flow = request.something
#     request(flow)



# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=6000)