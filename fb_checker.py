from requests import Session
from sys import argv
from fake_useragent import UserAgent


class FacebookChecker:

    # create the facebook checker object
    def __init__(self):
        self.session = Session()
        self.datr = None
        self.lsd = None
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgent().random,
        }

    # check if a phone number have an account
    def check_phone_number(self, phone_number):
        if phone_number[0] != '+':
            print(f"The phone number {phone_number} is not a valid phone number.")
            return False
        if self.check_identity(phone_number) == True:
            print(f"The phone number {phone_number} have an account!")
            return True
        print(f"The phone number {phone_number} doesn't have an account.")
        return False

    # check if an email have an account
    def check_email(self, email):
        if email.find('@') == -1:
            print(f"The email {email} is not a valid email.")
            return False
        if self.check_identity(email) == True:
            print(f"The email {email} have an account!")
            return True
        print(f"The email {email} doesn't have an account.")
        return False

    # check an identity (email or phone number)
    def check_identity(self, ident):

        # get the cookies
        if self.datr is None or self.lsd is None:
            if self.get_cookies() == False:
                return None

        # send the query
        url = 'https://www.facebook.com/ajax/login/help/identify.php'
        cookies = { 'datr': self.datr }
        data = { 'lsd': self.lsd, 'email': ident, '__a': '1' }
        response = self.session.post(url, cookies=cookies, data=data)

        # parse the response
        if response.status_code == 200:
            if response.text.find('?ldata=') != -1:
                return True
        return False

    # get the cookies from facebook
    def get_cookies(self):

        # query the cookie page
        url = 'https://www.facebook.com/login/'
        response = self.session.get(url, headers=self.headers)

        # parse the cookies
        self.datr = self.parse_cookie(response.text, '"_js_datr","')
        self.lsd = self.parse_cookie(response.text, '"token":"')

    # parse cookie from pattern
    def parse_cookie(self, text, pattern):
        pos = text.find(pattern)
        if pos == -1:
            return None
        pos += len(pattern)
        end_pos = text[pos:].find('"')
        if end_pos == -1:
            return None
        end_pos += pos
        return text[pos:end_pos]


# run the main function if needed
if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1][0] == '+':
            FacebookChecker().check_phone_number(argv[1])
            exit(0)
        elif argv[1].find('@') != -1:
            FacebookChecker().check_email(argv[1])
            exit(0)
    print("Usage: fb_checker.py <email or phone number>")
    exit(1)