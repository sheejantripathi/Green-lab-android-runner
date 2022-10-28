from mitmproxy import http, proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core
from bs4 import BeautifulSoup
from flask import Flask
import time
import pyshark
import time
import threading

POST_SERVER = "192.168.119.140"
POST_SERVER_PORT = 2222
POST_SERVER_URL = f"{POST_SERVER}:{POST_SERVER_PORT}"
LOCAL_SERVER_URL = "192.168.119.140:2222"
time_filename="/home/pi/mitmproxy_response.csv"
interface = 'wlan0'

# app = Flask(__name__)
class Sx5HTTPServer:
    time_start = 0
    time_end = 0
    packet_calculator = None

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Redirect HTTPS requests to example/ourserver 
        to our local webserver webserver 
        """
        website_list=[
            "wordpress", "amazon", "yahoo", "kickstarter", "youtube",
            "theatlantic", "udemy", "wikipedia", "skysports", "nbcnews",
            "alibabacloud", "stackoverflow", "bookmyshow", "archive", "mit",
            "pornhub", "pcgamer", "cic.gc.ca", "paypal", "tinder", "apkmirror"
        ]
        print('I am opening ' + flow.request.pretty_host)
        if any (website in flow.request.pretty_host for website in website_list): # and flow.request.path=="/ourserver":
            flow.request.headers["Host"] = flow.request.headers
            flow.request.host = POST_SERVER
            flow.request.port = POST_SERVER_PORT
            flow.request.scheme = "http"
            print('Forwarding request to ' + flow.request.host + ':'+ flow.request.port)
        else:
            print("I'm not in request list!")
        self.time_start = time.time()
        with open(time_filename, "a+") as f:
            f.write(flow.request.pretty_host+","+str(self.time_start))

        self.packet_calculator = Sx5NetworkPacketsCalculator(name=flow.request.pretty_host)
        self.packet_calculator.start_packet_capture(interface)

    def response(self, flow: http.HTTPFlow) -> None:
        js_snippet = 'function xml_http_post(url, data, callback) {         var req = new XMLHttpRequest();        req.open("POST", url, true) ;         req.send(data);    }    function calcaulate_performance() {        var plt = window.performance.timing.domComplete - window.performance.timing.requestStart;        console.log("Calculated PLT: " + plt);        xml_http_post('+'http://'+LOCAL_SERVER_URL+',  plt , null)    }    window.addEventListener ? window.addEventListener("load", calcaulate_performance, true) : window.attachEvent && window.attachEvent("onload", calcaulate_performance);'
        print("Currently, I'm in mitmproxy response...\n")
        # Add Javascript snippet to the body
        html = flow.response.get_text()
        self.time_end = time.time()
        with open(time_filename, "a+") as f:
            time_difference = self.time_end - self.time_start
            f.write(","+str(self.time_end)+","+str(time_difference)+"\n")
        #time_difference = self.time_end - self.time_start
        self.packet_calculator.stop_packet_capture()

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

packet_filename = "/home/pi/packet_capture.csv"
interface = 'wlan0'


class PacketCapture():
    capture = 1
    interface_name = ''
    total_packets_count = 0
    total_bytes_count = 0

    def __init__(self, interface_name):
        #threading.Thread.__init__(self)
        self.interface_name = interface_name
        #self._stop_event = threading.Event()


    def stop_execution(self):
        self.capture = 0
        print("Reached packet capture stop block!")
        # self.join()
        #self._stop_event.set()


    def task(self):
        packet_capture = pyshark.LiveCapture(interface=self.interface_name, bpf_filter='tcp port 80 || tcp port 443')
        try:
            for packet in packet_capture.sniff_continuously():
                if not self.capture:
                    packet_capture.close()
                    return
                print("New packets arriving in thread.start call")
                #
                # field_names = packet.tcp._all_fields
                # field_values = packet.tcp._all_fields.values()
                # for field_name in field_names:
                #     for field_value in field_values:
                #         if field_name == 'tcp.len':
                #             self.total_bytes_count += field_value
                self.total_packets_count += 1
                print(packet.length.size)
                self.total_bytes_count += int(packet.length.size)
        except Exception:
            self.exited = 1
            print("Capture has been closed because of TSharkCrashException!")


class Sx5NetworkPacketsCalculator:
    packet_capture = None
    packet_capture_thread = None
    name = ''

    def __init__(self, name):
        self.name = name

    def start_packet_capture(self, interface):
        self.packet_capture = PacketCapture(interface_name=interface)
        self.packet_capture_thread = threading.Thread(target=self.packet_capture.task)
        self.packet_capture_thread.start()
        print("I'm called in start before file-write")
        with open(packet_filename, "a+") as f:
            f.write(self.name+",")
        #return packet_capture
        #self.stop_packet_capture()


    def stop_packet_capture(self):
        try:
            self.packet_capture.stop_execution()
            #self.packet_capture_thread.kill()
            self.packet_capture_thread.join()
            #self.packet_capture.join()
            # for p in packet_capture:
            #     pass # read packet-size
            print("Almost stopped packet capture!")
        except:
            print("Sorry, can't do anything while thread termination was called and exception occurred!")
        finally:
            with open(packet_filename, "a+") as f:
                f.write("stop_packet_capture,"+ str(self.packet_capture.total_packets_count)+","+ str(self.packet_capture.total_bytes_count)+"\n")

