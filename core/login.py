import requests
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter
from core.encrypt import encrypt_pass, encrypt_user_id
from core.encode import encode_user_type, encode_user_id
from bs4 import BeautifulSoup
from PIL import Image
import io

class LegacyAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.options |= 0x4  # Enable legacy renegotiation
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# Creating session
session = requests.Session()
session.mount("https://", LegacyAdapter())

# Function to view login area
def view_login_area():
    
    # URL to view login area
    url = "https://banglarbhumi.gov.in/BanglarBhumi/viewLoginAreaAction"

    # Headers to be send to view login area request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/Home',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://banglarbhumi.gov.in',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    'Content-Length': '0',
    }

    
    # Response to view login area request
    response = session.post(url, headers=headers)
    
    # Function to get salt hash text from the view login area page using element id
    def get_salt_text():
        soup = BeautifulSoup(response.content, 'html.parser')
        element = soup.find(id="saltHashtext")
        salt_hash_text = element['value']
        
        # Returning salt hash txt value
        return salt_hash_text
    
    
    # Function to get cookies in string format
    def get_cookies():
        cookies_dict = session.cookies.get_dict()
        cookie_str = '; '.join(f"{key}={value}" for key, value in cookies_dict.items())
        return cookie_str
    
    
    # Function to generate login captcha
    def generate_login_captcha():
        url = "https://banglarbhumi.gov.in/BanglarBhumi/generateCaptcha"
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
        'Accept': 'image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/Home',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Cookie': get_cookies(),
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=5, i',
        }
        
        response = session.get(url, headers=headers)
        img = Image.open(io.BytesIO(response.content))
        img.show()
        
        
    generate_login_captcha()
    login_area_data = {
        'cookies': get_cookies(),
        'salt': get_salt_text(),
    }
    
    return login_area_data


# Function to generate login OTP
def generate_login_otp(username, password, salt, captcha, cookies):
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/loginOTPGenerationAction.action'
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/Home',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://banglarbhumi.gov.in',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Cookie': cookies,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    }

    data = {
    'userType': '2',
    'username': username,
    'txtInput': captcha,
    'password': encrypt_pass(password, salt),
    'saltHashtext': salt,
    'ajax': 'true',
    }   

    response = session.post(url, headers=headers, data=data)
    

# Function to validate login OTP
def validate_login_otp(username, password, salt, otp, cookies):
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/login.action'
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/Home',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://banglarbhumi.gov.in',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Cookie': cookies,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=0',
    }

    data = {
        'userType': encode_user_type('2'),
        'username': encode_user_id(username),
        'password': encrypt_pass(password, salt),
        'saltHashtext': salt,
        'retypepassword': encrypt_user_id(username, salt),
        'txtOTP': otp,
        'ajax': 'true',
    }

    response = session.post(url, headers=headers, data=data)
    data = response.json()
    return data