import requests
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter

class LegacyAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.options |= 0x4  # Enable legacy renegotiation
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# Creating session
session = requests.Session()
session.mount("https://", LegacyAdapter())

# Function to fetch districts
def fetch_districts():
    # URL to fetch districts
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/distPopulateAction_KUP.action'
    
    # Headers to be send to the fetch district request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://banglarbhumi.gov.in',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    }
    
    # Form data(payload) to be send to the fetch district request
    data = {
    'radioSelectionViewType': '1',
    'ajax': 'true',
    }
    
    # Response to the fetch district request
    response = session.post(url, headers=headers, data=data) # Response object(dictionary)
    # Parsing response object in JSON and extracting district list from JSON data
    district_obj_list = response.json()['districtList']
    
    # Returning list of district Objects
    return district_obj_list

# Function to fetch blocks
def fetch_blocks(dist_code):
    # URL to fetch blocks
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/blockPopulate_KUP.action'
    
    # Headers to be send to the fetch block request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://banglarbhumi.gov.in',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    }
    
    # Form data(payload) to send to the fetch block request
    data = {
    'lstDistrictCode1': dist_code,
    'radioSelectionViewType': '1',
    'ajax': 'true',
    }

    # # Response to the fetch block request
    response = session.post(url, headers=headers, data=data) # Response object(dictionary)
    # Parsing response object in JSON and extracting block list from JSON data
    block_obj_list = response.json()['blockList']
    
    # Returning list of Block Objects
    return block_obj_list

# Function to fetch mouzas
def fetch_mouzas(dist_code, block_code):
    # URL to fetch mouzas
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/mouzaPopulation_KUP.action'
    
    # Headers to be send to the fetch mouzas request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://banglarbhumi.gov.in',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    }
    
    # Form data(payload) to be send to the fetch mouzas request
    data = {
    'lstDistrictCode1': dist_code,
    'lstBlockCode1': block_code,
    'radioSelectionViewType': '1',
    'ajax': 'true',
    }

    # Response to the fetch mouzas request
    response = session.post(url, headers=headers, data=data) # Response object(dictionary)
    mouza_obj_list = response.json()['mouzaList'] # Parsing response object in JSON and extracting mouza list from JSON data

    # Returning List of Mouza objects
    return mouza_obj_list

# Function to fetch khatian info
def fetch_khatian(cookies, dist_code, block_code, mouza_code, khatian_no, bata_khatian_no=""):
    # URL to fetch khatian info
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/khDetailsAction_LandInfo.action'
    
    # Headers to be send to the fetch khatian info request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action',
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

    # Form data(payload) to be send to the fetch khatian info request
    data = {
    'lstDistrictCode1': dist_code,
    'lstBlockCode1': f"{block_code}_NEW",
    'lstMouzaList': mouza_code,
    'txtKhatian1': khatian_no,
    'txtKhatian2': bata_khatian_no,
    'radioKhatianDtlType': '0',
    'yourLang': 'bn_in',
    'ajax': 'true',
    }

    # Response to the fetch khatian info request
    response = session.post(url, headers=headers, data=data) # Response object(dictionary)
    khatian_info = response.json()["msgShow"] # Parsing response object in JSON and extracting khatian info from JSON data
    
    # Returning khatian info in HTML format
    return khatian_info

# Function to fetch plot info
def fetch_plot(cookies, dist_code, block_code, mouza_code, plot_no, bata_plot_no=""):
    # URL to fetch plot info
    url = 'https://banglarbhumi.gov.in/BanglarBhumi/plotDetailsAction_LandInfo.action'
    
    # Headers to be send to the fetch plot info request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action',
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

    # Form data(payload) to be send to the fetch plot info request
    data = {
    'lstDistrictCode1': dist_code,
    'lstBlockCode1': f"{block_code}_NEW",
    'lstMouzaList': mouza_code,
    'txtPlotNo': plot_no,
    'txtBataPlotNo': bata_plot_no,
    'radioKhatianDtlType': '0',
    'yourLang': 'bn_in',
    'ajax': 'true',
    }

    # Response to the fetch plot info request
    response = session.post(url, headers=headers, data=data) # Response object(dictionary)
    plot_info = response.json()["msgShow"] # Parsing response object in JSON and extracting plot info from JSON data
    
    # Returning plot info in HTML format
    return plot_info
