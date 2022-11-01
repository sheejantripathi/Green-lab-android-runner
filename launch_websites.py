import subprocess
import time


def launch_website():
	list_of_websites = ["https://www.wordpress.org", "https://www.amazon.com", "https://finance.yahoo.com", "https://www.kickstarter.com", "https://www.youtube.com",
    "https://www.theatlantic.com", "https://udemy.com", "https://www.wikipedia.com", "https://www.skysports.com", "https://www.nbcnews.com",
    "https://alibabacloud.com", "https://www.stackoverflow.com", "https://www.bookmyshow.com", "https://archive.org", "https://www.mit.edu",
    "https://www.pornhub.com", "https://www.pcgamer.com", "https://www.cic.gc.ca", "https://www.paypal.com", "https://www.tinder.com"]
	for name in list_of_websites:
		browser_execution(name, "Chrome")
		time.sleep(12)


def browser_execution(name, browser_name):
	intermediary_cmd = ''
	if browser_name == "Chrome":
		intermediary_cmd = 'com.android.chrome/com.google.android.apps.chrome.Main'
	elif browser_name == "Firefox":
		intermediary_cmd = 'org.mozilla.firefox/org.mozilla.gecko.BrowserApp'
	elif browser_name == "Brave":
		intermediary_cmd = 'com.brave.browser/com.google.android.apps.chrome.Main'
	elif browser_name == "Opera":
		intermediary_cmd = 'com.opera.browser/com.opera.Opera'
	subprocess.run(f"adb shell am start -n {intermediary_cmd} -d {name}", shell=True, check=True)
	#subprocess.run("adb shell input keyevent 4", shell=True, check=True)


if __name__ == '__main__':
	launch_website()
