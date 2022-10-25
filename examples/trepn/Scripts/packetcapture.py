import pyshark

interface = "sshdump"
capture=None

def start_capture():
	global capture = pyshark.LiveCapture(interface=interface, output_file=os.path.join('tmp','packet_log'))
	pass


def stop_capture():
	global capture.clear()
	global capture.close
	pass