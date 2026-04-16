from bs4 import BeautifulSoup
from PIL import Image
import io

from ..api import api_urls
from ..security import encrypt_password, encrypt_user_id, encode_user_id, encode_user_type
from ..services import session


class LoginService:
    """Login Service"""
    
    def __init__(self):
        self.cookies = ""
        self.salt = ""
        self.captcha = None
        self.response = None
        self.view_login_area()
        
        # print(self.salt)

    def view_login_area(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/Home",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://banglarbhumi.gov.in",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Priority": "u=0",
                "Content-Length": "0",
            }

            response = session.post(api_urls.get("login_area_url"), headers=headers)

            self.response = response
            self.salt = self.get_salt_text()
            self.cookies = self.get_cookies()
            self.captcha = self.generate_captcha()

        except Exception as e:
            print(e)
            

    def get_salt_text(self) -> str:
        """Extract salt hash text from login area HTML"""

        soup = BeautifulSoup(self.response.content, "lxml")
        element = soup.find(id="saltHashtext")
        salt_text = element["value"]

        return salt_text
    

    def get_cookies(self) -> str:
        """Extract cookies in string format from the login session"""

        cookies_dict = session.cookies.get_dict()
        cookies = "; ".join(f"{key}={value}" for key, value in cookies_dict.items())

        return cookies
    

    def generate_captcha(self):
        """Generate Captcha"""
        """To refresh captcha call generate_captcha method(with existing cookies as many times you want).
        Don't need to update cookies(no need of new cookies)
        
        CODE:
        login = LoginService()
        login.generate_captcha() # To refresh captcha
        """
        
        try:
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/Home",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=5, i",
            }

            response = session.get(api_urls.get("generate_captcha_url"), headers=headers)
            captcha = Image.open(io.BytesIO(response.content))
            # captcha.show()
            return captcha
        
        except Exception as e:
            print(e)
            raise
    

    def generate_otp(self, username: str, password: str, captcha: str):
        """Generate OTP"""
        
        try:
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
            'Cookie': self.cookies,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
            }

            data = {
            'userType': '2',
            'username': username,
            'txtInput': captcha,
            'password': encrypt_password(password, self.salt),
            'saltHashtext': self.salt,
            'ajax': 'true',
            }   

            response = session.post(api_urls.get("generate_otp_url"), headers=headers, data=data)
            response_data = response.json()
            
            return response_data
            
        except Exception as e:
            print(e)
            raise
        
    
    def validate_otp(self, username: str, password: str, otp: str):
        """Validate OTP and LOGIN"""
        
        try:
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
            'Cookie': self.cookies,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
            }

            data = {
                'userType': encode_user_type('2'),
                'username': encode_user_id(username),
                'password': encrypt_password(password, self.salt),
                'saltHashtext': self.salt,
                'retypepassword': encrypt_user_id(username, self.salt),
                'txtOTP': otp,
                'ajax': 'true',
            }

            response = session.post(api_urls.get("validate_otp_url"), headers=headers, data=data)
            response_data = response.json()
            
            return response_data

    
        except Exception as e:
            print(e)
            raise
    
