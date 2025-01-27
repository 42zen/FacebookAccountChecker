import requests
import sys


# you don't need an account to get theses ;)
FACEBOOK_DATR = 'AuWXZ6h2pspMJrfUZ_yz8ps8'
FACEBOOK_LSD ='AVrNCasKB3s' 


# check an identity (email or phone number)
def check_identity(ident):
    url = 'https://www.facebook.com/ajax/login/help/identify.php'
    cookies = { 'datr': FACEBOOK_DATR }
    data = { 'lsd': FACEBOOK_LSD, 'email': ident, '__a': '1' }

    response = requests.post(url, cookies=cookies, data=data )

    if response.status_code == 200:
        if response.text.find('?ldata=') != -1:
            return True
    return False

# check if a phone number have an account
def check_phone_number(phone_number):
    if phone_number[0] != '+':
        print(f"The phone number {phone_number} is not a valid phone number.")
        return False
    if check_identity(phone_number) == True:
        print(f"The phone number {phone_number} have an account!")
        return True
    print(f"The phone number {phone_number} doesn't have an account.")
    return False

# check if an email have an account
def check_email(email):
    if email.find('@') == -1:
        print(f"The email {email} is not a valid email.")
        return False
    if check_identity(email) == True:
        print(f"The email {email} have an account!")
        return True
    print(f"The email {email} doesn't have an account.")
    return False


# run the main function if needed
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1][0] == '+':
            check_phone_number(sys.argv[1])
            exit(0)
        elif sys.argv[1].find('@') != -1:
            check_email(sys.argv[1])
            exit(0)
    print("Usage: fb_checker.py <email or phone number>")
    exit(1)