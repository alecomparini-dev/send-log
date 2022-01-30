import requests
import logging as logging

from dotenv import dotenv_values
from model.transaction_log import TransactionLog
from service.log import LogService
from service.oauth import OAuthService

config = dotenv_values(".env")
oauth = OAuthService(config['URL_TOKEN'], config['CLIENT_ID'], config['CLIENT_SECRET'])
log_service = LogService(config['URL_LOG'], oauth)


def process_transaction():
    logging.basicConfig(filename=config['PATH_LOG_ERROR'], filemode='w',
                        format='%(levelname)s - %(asctime)s - %(message)s',
                        level=logging.INFO)

    logging.info("Started processing...")

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

                try:
                    log_service.send_log(log)
                except Exception as e:
                    logging.error(f'`Exception Error: {e} - Request:{str(requests)} - Line:{str(nro_line)}')
                    reprocess(log)

    except IOError as e:
        logging.error(msg=str(e), exc_info=True)

    logging.info(f'Process finished - Total lines processed: {nro_line}')


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


if __name__ == '__main__':
    process_transaction()
