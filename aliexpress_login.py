import pickle
from selenium import webdriver

browser = webdriver.Firefox()


def get_cookies():
    browser.get("https://login.aliexpress.com/?flag=1&return_url=http%3A%2F%2Fportals.aliexpress.com%2Fhelp.htm%3Fpage%3Dhelp_center%26toMenu%3DtopQuestions")
    print('input your username and password in Firefox and hit Submit')
    input('Hit Enter here if you have summited the form: <Enter>')
    cookies = browser.get_cookies()
    pickle.dump(cookies, open("cookies.pickle", "wb"))


def set_cookies():
    browser.get("https://aliexpress.com")
    cookies = pickle.load(open("cookies.pickle", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get("https://bestselling.aliexpress.com/en")


if __name__ == '__main__':
    get_cookies()
