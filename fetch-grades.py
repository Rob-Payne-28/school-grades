import requests
import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(filename='grades_script.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

try:
    login_page_url = os.environ.get('LOGIN_PAGE_URL')
    login_action_url = os.environ.get('LOGIN_ACTION_URL')
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    baseUrl = os.environ.get('I_FRAME_URL')
    user_agent_string = os.environ.get('USER_AGENT')

    session = requests.Session()
    session.headers.update({'User-Agent': user_agent_string})

    response = session.get(login_page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')

    login_data = {
        '__RequestVerificationToken': token,
        'SCKTY00328510CustomEnabled': 'False',
        'SCKTY00436568CustomEnabled': 'False',
        'Database': '10',
        'VerificationOption': 'UsernamePassword',
        'LogOnDetails.UserName': username,
        'tempUN': '',
        'tempPW': '',
        'LogOnDetails.Password': password
    }

    headers = {
        'User-Agent': user_agent_string,
        'Referer': login_page_url,
    }

    logging.info("Attempting to authenticate...")
    login_response = session.post(login_action_url, data=login_data, headers=headers)
    login_response.raise_for_status()
    soup = BeautifulSoup(login_response.text, 'html.parser')

    if login_response.ok:
        logging.info("Authentication successful.")
    else:
        logging.error(f"Authentication failed. Status code: {login_response.status_code}")

    logging.info("Getting updated grades...")

    iframe = soup.find('iframe', id='sg-legacy-iframe')
    iframe_url = iframe['src'] if iframe else None

    if iframe_url:
        if not iframe_url.startswith('http'):
            iframe_url = baseUrl + iframe_url

        iframe_response = session.get(iframe_url)
        iframe_response.raise_for_status()

        soup = BeautifulSoup(iframe_response.text, 'html.parser')
        table = soup.find('table', {'id': 'plnMain_dgIPR'})

        if table:
            header_row = table.find('thead') or table.find('tr')
            headers = [header.text.strip() for header in header_row.find_all(['th', 'td'])]

            data_list = []
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                row_data = {header: col.text.strip() for header, col in zip(headers, cols)}
                data_list.append(row_data)

            comment_legend_table = soup.find('table', {'id': 'plnMain_dgCommentLegend'})
            comment_legend = {}
            if comment_legend_table:
                for row in comment_legend_table.find_all('tr')[1:]:  # Skipping the header
                    code, description = [td.text.strip() for td in row.find_all('td')]
                    comment_legend[code] = description

            for row_data in data_list:
                for key in ['CM1', 'CM2']:
                    if row_data[key] in comment_legend:
                        row_data[key] = comment_legend[row_data[key]]

            json_data = json.dumps(data_list, indent=4)
            print(json_data)
        else:
            logging.error("Table not found")
    else:
        logging.error("iframe not found")

except requests.exceptions.RequestException as e:
    logging.error(f"Request error: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
