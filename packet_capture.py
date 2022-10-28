import pyshark
import time
import threading

filename = "/home/pi/packet_capture.csv"
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

    def __init__(self, hostname):
        self.name = hostname

    def start_packet_capture(self, interface):
        self.packet_capture = PacketCapture(interface_name=interface)
        self.packet_capture_thread = threading.Thread(target=self.packet_capture.task)
        self.packet_capture_thread.start()
        print("I'm called in start before file-write")
        with open(filename, "a+") as f:
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
            with open(filename, "a+") as f:
                f.write("stop_packet_capture,"+ str(self.packet_capture.total_packets_count)+","+ str(self.packet_capture.total_bytes_count)+"\n")


    # def count_packets(filename):
    #     filename=''
    #     cap = pyshark.FileCapture(filename, bpf_filter='tcp port 80 || tcp port 443')
    #     i = 0
    #     for idx, packet in enumerate(cap):
    #         i += 1
    #     print(i)
    #     print(len(cap._packets))


def main():
    try:
        print('I\'m the main function')
        packet_calculator = Sx5NetworkPacketsCalculator()
        packet_calculator.start_packet_capture(interface)
        # print('Sleeping for 2 seconds...')
        time.sleep(25)
        print('Just woke up, finishing my job!')
        packet_calculator.stop_packet_capture()
    except:
        print("Sorry! We can't do anything!!")
    

# if __name__ == '__main__':
#     main()