import logging

from .api_urls import API_URLs as api_urls
from ..services import session


def fetch_districts() -> list:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://banglarbhumi.gov.in",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        data = {
            "radioSelectionViewType": "1",
            "ajax": "true",
        }

        response = session.post(
            api_urls.get("district_url"), headers=headers, data=data
        )
        district_list = response.json().get("districtList")

        return district_list

    except Exception as e:
        logging.exception(e)
        raise


def fetch_blocks(district_code: str) -> list:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://banglarbhumi.gov.in",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0",
        }

        data = {
            "lstDistrictCode1": district_code,
            "radioSelectionViewType": "1",
            "ajax": "true",
        }

        response = session.post(api_urls.get("block_url"), headers=headers, data=data)
        block_list = response.json().get("blockList")

        return block_list

    except Exception as e:
        logging.exception(e)
        raise


def fetch_mouzas(district_code: str, block_code: str) -> list:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/KnowYourProperty.action",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://banglarbhumi.gov.in",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0",
        }

        data = {
            "lstDistrictCode1": district_code,
            "lstBlockCode1": block_code,
            "radioSelectionViewType": "1",
            "ajax": "true",
        }

        response = session.post(api_urls.get("mouza_url"), headers=headers, data=data)
        mouza_list = response.json().get("mouzaList")

        return mouza_list

    except Exception as e:
        logging.exception(e)
        raise
    
    
def fetch_khatian(cookies: str, district_code: str, block_code: str, mouza_code: str, khatian_no: str, bata_khatian_no="") -> str:
    try:
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

        data = {
        'lstDistrictCode1': district_code,
        'lstBlockCode1': f"{block_code}_NEW",
        'lstMouzaList': mouza_code,
        'txtKhatian1': khatian_no,
        'txtKhatian2': bata_khatian_no,
        'radioKhatianDtlType': '0',
        'yourLang': 'bn_in',
        'ajax': 'true',
        }

        response = session.post(api_urls.get("khatian_url"), headers=headers, data=data)
        khatian_info = response.json().get("msgShow")
        
        return khatian_info

    except Exception as e:
        logging.exception(e)
        raise
    

def fetch_plot(cookies: str, district_code: str, block_code: str, mouza_code: str, plot_no: str, bata_plot_no="") -> str:
    try:
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

        data = {
        'lstDistrictCode1': district_code,
        'lstBlockCode1': f"{block_code}_NEW",
        'lstMouzaList': mouza_code,
        'txtPlotNo': plot_no,
        'txtBataPlotNo': bata_plot_no,
        'radioKhatianDtlType': '0',
        'yourLang': 'bn_in',
        'ajax': 'true',
        }

        response = session.post(api_urls.get("plot_url"), headers=headers, data=data)
        plot_info = response.json().get("msgShow")

        return plot_info
    
    except Exception as e:
        logging.exception(e)
        raise