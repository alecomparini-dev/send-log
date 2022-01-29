import requests
import logging as logging
from oauth import OAuth
from model.transaction_log import TransactionLog
from dotenv import dotenv_values

config = dotenv_values(".env")
oauth = OAuth()


def send_log():
    logging.basicConfig(filename=config['PATH_LOG_ERROR'], filemode='w',
                        format='%(levelname)s - %(asctime)s - %(message)s',
                        level=logging.INFO)

    logging.info("Started processing...")

    url = config['URL_LOG']
    path_log = config['PATH_LOG']
    nro_line = 0

    try:
        with open(path_log, "rt", encoding='utf-8') as file:
            for line in file:
                nro_line += 1

                if not line_is_valid(line):
                    continue

                content = line.strip().split(";")

                log = TransactionLog(brand=content[0],
                                     transaction_date=content[1],
                                     client=content[2],
                                     amount=content[3])

                send(url, log, nro_line)

    except IOError as e:
        logging.error(msg=str(e), exc_info=True)

    logging.info("Process finished")


def send(url, log, nro_line):
    headers = config_headers()
    response = requests.post(url=url, json=log.__dict__, headers=headers)
    if not validate_response(log.__dict__, response, nro_line):
        reprocess(log)


def validate_response(req, resp, nro_line):

    msg_default = f'Status:{str(resp.status_code)} - Request:{req} - Response: {str(resp.json())} - Line:{str(nro_line)} '

    if 400 <= resp.status_code < 500:
        msg = 'Request Error'
        logging.warning(msg=f'{msg} - {msg_default}')
        return False
    elif 500 <= resp.status_code < 600:
        msg = 'Server Error'
        logging.warning(msg=f'{msg} - {msg_default}')
        return False

    return True


def reprocess(log):
    path = config['PATH_REPROCESS']
    line = log.convert_to_txt(log.brand, log.transactionDate, log.client, log.amount)
    with open(path, "a", encoding='utf-8') as file:
        file.write(line + '\n')


def line_is_valid(line):
    if len(line.strip()) == 0:
        return False

    if len(line.strip().split(";")) < 4:
        return False

    return True


def config_headers():
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + oauth.token
    }


if (__name__ == '__main__'):
    send_log()
