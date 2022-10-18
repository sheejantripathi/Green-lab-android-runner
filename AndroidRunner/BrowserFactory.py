from .Browsers import Chrome, Firefox, Opera, Brave


class BrowserFactory(object):
    @staticmethod
    def get_browser(name):
        if name == "chrome":
            return Chrome.Chrome
        if name == "firefox":
            return Firefox.Firefox
        if name == "opera":
            return Opera.Opera
        if name == "brave":
            return Brave.Brave
        raise Exception("No Browser found")
