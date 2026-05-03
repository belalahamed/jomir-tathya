import logging
from ..services import session


def fetch_districts():
    """Fetch Districts List"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/distPopulateAction_KUP.action"

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

    try:
        response = session.post(url=url, headers=headers, data=data)
        district_list = response.json().get("districtList")
        return district_list
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise


def fetch_blocks(district_code: str):
    """Fetch Blocks List"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/blockPopulate_KUP.action"

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

    try:
        response = session.post(url=url, headers=headers, data=data)
        block_list = response.json().get("blockList")
        return block_list
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise


def fetch_mouzas(district_code: str, block_code: str):
    """Fetch Mouzas List"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/mouzaPopulation_KUP.action"

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

    try:
        response = session.post(url=url, headers=headers, data=data)
        mouza_list = response.json().get("mouzaList")
        return mouza_list
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise


def fetch_khatian(
    cookies: str,
    district_code: str,
    block_code: str,
    mouza_code: str,
    khatian_no: str,
    bata_khatian_no="",
):
    """Fetch Khatian Information"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/khDetailsAction_LandInfo.action"

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
        "Cookie": cookies,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
    }

    data = {
        "lstDistrictCode1": district_code,
        "lstBlockCode1": f"{block_code}_NEW",
        "lstMouzaList": mouza_code,
        "txtKhatian1": khatian_no,
        "txtKhatian2": bata_khatian_no,
        "radioKhatianDtlType": "0",
        "yourLang": "bn_in",
        "ajax": "true",
    }

    try:
        response = session.post(url=url, headers=headers, data=data)
        khatian_info = response.json().get("msgShow")
        return khatian_info
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise


def fetch_plot(
    cookies: str,
    district_code: str,
    block_code: str,
    mouza_code: str,
    plot_no: str,
    bata_plot_no="",
):
    """Fetch Plot Information"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/plotDetailsAction_LandInfo.action"

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
        "Cookie": cookies,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
    }

    data = {
        "lstDistrictCode1": district_code,
        "lstBlockCode1": f"{block_code}_NEW",
        "lstMouzaList": mouza_code,
        "txtPlotNo": plot_no,
        "txtBataPlotNo": bata_plot_no,
        "radioKhatianDtlType": "0",
        "yourLang": "bn_in",
        "ajax": "true",
    }

    try:
        response = session.post(url=url, headers=headers, data=data)
        plot_info = response.json().get("msgShow")
        return plot_info
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise


def fetch_plot_mutation_status(
    cookies: str,
    district_code: str,
    block_code: str,
    mouza_code: str,
    plot_no: str,
    bata_plot_no="",
):
    """Fetch Plot Information"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/plotKhatianWiseStatusAction_LandInfo.action"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/PlotKhatianStatus.action",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://banglarbhumi.gov.in",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Cookie": cookies,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
    }

    data = {
        "idn": f"{district_code}{block_code}{mouza_code}",
        "txtPlotNo": plot_no,
        "txtBataPlotNo": bata_plot_no,
        "radioMuteMenuType": "1",
        "ajax": "true",
    }

    try:
        response = session.post(url=url, headers=headers, data=data)
        plot_mutation_info = response.json().get("msgShow")
        return plot_mutation_info
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise
    

def fetch_khatian_mutation_status(
    cookies: str,
    district_code: str,
    block_code: str,
    mouza_code: str,
    plot_no: str,
    bata_plot_no="",
):
    """Fetch Plot Information"""

    url = "https://banglarbhumi.gov.in/BanglarBhumi/plotKhatianWiseStatusAction_LandInfo.action"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://banglarbhumi.gov.in/BanglarBhumi/PlotKhatianStatus.action",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://banglarbhumi.gov.in",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Cookie": cookies,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
    }

    data = {
        "idn": f"{district_code}{block_code}{mouza_code}",
        "txtPlotNo": plot_no,
        "txtBataPlotNo": bata_plot_no,
        "radioMuteMenuType": "2",
        "ajax": "true",
    }

    try:
        response = session.post(url=url, headers=headers, data=data)
        plot_mutation_info = response.json().get("msgShow")
        return plot_mutation_info
    except Exception as e:
        logging.exception("An error occurred: ", e)
        raise