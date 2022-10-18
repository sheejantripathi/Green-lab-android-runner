from .Browser import Browser


class Brave(Browser):
    def __init__(self):
        super(Brave, self).__init__('com.brave.browser', 'com.google.android.apps.chrome.Main')

