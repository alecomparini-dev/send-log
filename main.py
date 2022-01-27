import requests
import logging as logging
from oauth import OAuth
from model.transaction_log import TransactionLog
from dotenv import dotenv_values

logging.basicConfig(filename='log/app.log', filemode='w', format='%(levelname)s - %(asctime)s - %(message)s',
                    level=logging.INFO)

config = dotenv_values(".env")
oauth = OAuth()


def send_log():
    logging.info("Started processing...")
    url = config['URL_LOG']
    nro_line = 0
    try:
        with open("log/transactions.txt", "rt", encoding='utf-8') as file:
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

    logging.info("Finished process")


def send(url, log, nro_line):
    headers = config_headers()

    try:
        # response = requests.get(url=url,headers=headers)
        response = requests.delete(url=url, json=log.__dict__, headers=headers)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(str(e))
        logging.warning(msg=f'{str(e)} - Line:{str(nro_line)} - StatusCode: {str(response.status_code)}')
        reprocess(log)
    except requests.exceptions.Timeout or requests.exceptions.ConnectTimeout as e:
        print(str(e))
        logging.warning(msg=f'{str(e)} - Line:{str(nro_line)} - StatusCode: {str(response.status_code)}')
        reprocess(log)
    except Exception as e:
        print(str(e))
        logging.error(msg=f'{str(e)} - Line:{str(nro_line)} - StatusCode: {str(response.status_code)}', exc_info=True)


def reprocess(log):
    print(log)
    line = log.convert_to_txt(log.brand, log.transaction_date, log.client, log.amount)

    with open("log/reprocess/reprocess.txt", "a", encoding='utf-8') as file:
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

# token_n = 'eyJraWQiOiJiNGVIeHFZSzRDc1paNVByZDlNSVhTTzlwOGY3OURWdmwyRVlpTm55WFRBPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3cDN0cnRhcm9oMHB2MXA3ZnNhaTE5bG1oaiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiY2FyYWRocmFzXC9jYXJkcyBjYXJhZGhyYXNcL2VmdCBjYXJhZGhyYXNcL3JlYWQgY2FyYWRocmFzXC9hanVzdGVzLWZpbmFuY2Vpcm9zIGNhcmFkaHJhc1wvdGFyaWZmIGNhcmFkaHJhc1wvc3BsaXQgY2FyYWRocmFzXC93YXJtdXAgY2FyYWRocmFzXC9hdXRob3JpemVyIGNhcmFkaHJhc1wvSW5kaXZpZHVhbHMtdjEgY2FyYWRocmFzXC9iaWxsZXQgY2FyYWRocmFzXC9pbmRpdmlkdWFsc1Bvc3QgY2FyYWRocmFzXC9waXgtYmFhcyBjYXJhZGhyYXNcL2xvY2stZnVuZHMgY2FyYWRocmFzXC93ZWJob29rIGNhcmFkaHJhc1wvZ2VuZXJhdGVkb2N1bWVudCBjYXJhZGhyYXNcL2NyeXB0IGNhcmFkaHJhc1wvcDJwdHJhbnNmZXIgY2FyYWRocmFzXC9vbW5pY2hhbm5lbCBjYXJhZGhyYXNcL3VzZXIgY2FyYWRocmFzXC9hbnRpZnJhdWQgY2FyYWRocmFzXC9kb2NrLW9uZ29pbmcgY2FyYWRocmFzXC90cmFuc3BvcnRjYXJkcyBjYXJhZGhyYXNcL3dyaXRlIGNhcmFkaHJhc1wvYmFua3RyYW5zZmVycyBjYXJhZGhyYXNcL3BheW1lbnRzIGNhcmFkaHJhc1wvcmVjaGFyZ2VzIGNhcmFkaHJhc1wvY2R0LWF1dGhvcml6ZXIgY2FyYWRocmFzXC9hY2NvdW50LXBkZiBjYXJhZGhyYXNcL2NhcnRvZXMgY2FyYWRocmFzXC9zaW5nbGUtaXNzdWVyIiwiYXV0aF90aW1lIjoxNjQzMjE2ODA0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9YNnNVbnZqNG4iLCJleHAiOjE2NDMyMjA0MDQsImlhdCI6MTY0MzIxNjgwNCwidmVyc2lvbiI6MiwianRpIjoiYjljNjdmZDUtNzY3Yy00OGNiLTgyYjItNWZjMGQ3YmNmOWJmIiwiY2xpZW50X2lkIjoiN3AzdHJ0YXJvaDBwdjFwN2ZzYWkxOWxtaGoifQ.1fR8P7KKgMGQDvgU4MIqUlCk74ccyq94drmwX9-hlvkS5wYYxQoRtmlNwyppzSUPcDqNWXWNhI8c1ncQXHBG7OOhmDUR4u4TVM1gdnyOWFwNqz4lwm4yVjWdawoQareg7sO01joFMuUE25-uSLLg3d-0zu4MZKrgX_CfXcSy0GL1T5ighONdJiXID7yuG6yIglh6jHG9Dat9SVwN7Rnb4KoUaPa9LvCAotL3KkYIorK0e79dkI2-hZ40sKIu30uydiI8kdo7IcGmtGVBd1T4l6i2CiGqbTtGA1v9nzNgh_T9UiEqcAO8g-2WJTsJkMzzfmzGGOpffPDvbcH4reTbIw'
# token_1 = 'eyJraWQiOiJiNGVIeHFZSzRDc1paNVByZDlNSVhTTzlwOGY3OURWdmwyRVlpTm55WFRBPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3cDN0cnRhcm9oMHB2MXA3ZnNhaTE5bG1oaiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiY2FyYWRocmFzXC9jYXJkcyBjYXJhZGhyYXNcL2VmdCBjYXJhZGhyYXNcL3JlYWQgY2FyYWRocmFzXC9hanVzdGVzLWZpbmFuY2Vpcm9zIGNhcmFkaHJhc1wvdGFyaWZmIGNhcmFkaHJhc1wvc3BsaXQgY2FyYWRocmFzXC93YXJtdXAgY2FyYWRocmFzXC9hdXRob3JpemVyIGNhcmFkaHJhc1wvSW5kaXZpZHVhbHMtdjEgY2FyYWRocmFzXC9iaWxsZXQgY2FyYWRocmFzXC9pbmRpdmlkdWFsc1Bvc3QgY2FyYWRocmFzXC9waXgtYmFhcyBjYXJhZGhyYXNcL2xvY2stZnVuZHMgY2FyYWRocmFzXC93ZWJob29rIGNhcmFkaHJhc1wvZ2VuZXJhdGVkb2N1bWVudCBjYXJhZGhyYXNcL2NyeXB0IGNhcmFkaHJhc1wvcDJwdHJhbnNmZXIgY2FyYWRocmFzXC9vbW5pY2hhbm5lbCBjYXJhZGhyYXNcL3VzZXIgY2FyYWRocmFzXC9hbnRpZnJhdWQgY2FyYWRocmFzXC9kb2NrLW9uZ29pbmcgY2FyYWRocmFzXC90cmFuc3BvcnRjYXJkcyBjYXJhZGhyYXNcL3dyaXRlIGNhcmFkaHJhc1wvYmFua3RyYW5zZmVycyBjYXJhZGhyYXNcL3BheW1lbnRzIGNhcmFkaHJhc1wvcmVjaGFyZ2VzIGNhcmFkaHJhc1wvY2R0LWF1dGhvcml6ZXIgY2FyYWRocmFzXC9hY2NvdW50LXBkZiBjYXJhZGhyYXNcL2NhcnRvZXMgY2FyYWRocmFzXC9zaW5nbGUtaXNzdWVyIiwiYXV0aF90aW1lIjoxNjQzMjEyMzgxLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9YNnNVbnZqNG4iLCJleHAiOjE2NDMyMTU5ODEsImlhdCI6MTY0MzIxMjM4MSwidmVyc2lvbiI6MiwianRpIjoiMjliNmFjMjctMzZiYi00MGM5LTgyMmQtZWZjMmNhNDJjZWIwIiwiY2xpZW50X2lkIjoiN3AzdHJ0YXJvaDBwdjFwN2ZzYWkxOWxtaGoifQ.H1_OzJoN3V2AlMj-w8t6jGVB2D8XCY8bb4mNjM_2hk_M4Z32R9_5vk1V22mgD6OLDL8ZnnJqR1j-CWPgUYS49iia_g9KzLvnnZfE-NrMhr-4d3p-aO5Gxn0NpQGjMm9PogZmAhr_JZ94mVrgnYHsDd18_e-GnhOE15pw5PwNa0WHqpMyM6od6h4GQwzabjl2Iyg7oByYmDK3vpZ4oBJfqvM3f0ZZjmNtB_o4UuJgdPDQsRAI9KiPGFcz25HkF_EccUhsOrvzkHQcLhDWcfRW63phErZafVVN78METxGAZKs-UspMPgQl2yqfRQ0vduuDSMMSAW94lyqSCLoya11Btw'
# token_2 = 'eyJraWQiOiJiNGVIeHFZSzRDc1paNVByZDlNSVhTTzlwOGY3OURWdmwyRVlpTm55WFRBPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3cDN0cnRhcm9oMHB2MXA3ZnNhaTE5bG1oaiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiY2FyYWRocmFzXC9jYXJkcyBjYXJhZGhyYXNcL2VmdCBjYXJhZGhyYXNcL3JlYWQgY2FyYWRocmFzXC9hanVzdGVzLWZpbmFuY2Vpcm9zIGNhcmFkaHJhc1wvdGFyaWZmIGNhcmFkaHJhc1wvc3BsaXQgY2FyYWRocmFzXC93YXJtdXAgY2FyYWRocmFzXC9hdXRob3JpemVyIGNhcmFkaHJhc1wvSW5kaXZpZHVhbHMtdjEgY2FyYWRocmFzXC9iaWxsZXQgY2FyYWRocmFzXC9pbmRpdmlkdWFsc1Bvc3QgY2FyYWRocmFzXC9waXgtYmFhcyBjYXJhZGhyYXNcL2xvY2stZnVuZHMgY2FyYWRocmFzXC93ZWJob29rIGNhcmFkaHJhc1wvZ2VuZXJhdGVkb2N1bWVudCBjYXJhZGhyYXNcL2NyeXB0IGNhcmFkaHJhc1wvcDJwdHJhbnNmZXIgY2FyYWRocmFzXC9vbW5pY2hhbm5lbCBjYXJhZGhyYXNcL3VzZXIgY2FyYWRocmFzXC9hbnRpZnJhdWQgY2FyYWRocmFzXC9kb2NrLW9uZ29pbmcgY2FyYWRocmFzXC90cmFuc3BvcnRjYXJkcyBjYXJhZGhyYXNcL3dyaXRlIGNhcmFkaHJhc1wvYmFua3RyYW5zZmVycyBjYXJhZGhyYXNcL3BheW1lbnRzIGNhcmFkaHJhc1wvcmVjaGFyZ2VzIGNhcmFkaHJhc1wvY2R0LWF1dGhvcml6ZXIgY2FyYWRocmFzXC9hY2NvdW50LXBkZiBjYXJhZGhyYXNcL2NhcnRvZXMgY2FyYWRocmFzXC9zaW5nbGUtaXNzdWVyIiwiYXV0aF90aW1lIjoxNjQzMjEyNjE1LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9YNnNVbnZqNG4iLCJleHAiOjE2NDMyMTYyMTUsImlhdCI6MTY0MzIxMjYxNSwidmVyc2lvbiI6MiwianRpIjoiYTg4MDgzYzMtZWFjMi00MWJhLTk5N2QtYjAwY2U5Y2Y2NWMyIiwiY2xpZW50X2lkIjoiN3AzdHJ0YXJvaDBwdjFwN2ZzYWkxOWxtaGoifQ.0C3XiIbOxt6VrdKvEULEByKCsN-XMvyiulqviBcSxSHNvAaXi0EhbDtcLjFc1pkVt0ShqVAb4B1Zz0AGIEUYquoTCvr8qzoxyMhmLHb1tLgVfpD498Gofc5uzX5Cn5IuCMdmD6RGuHp5uAmAZBzREYMQIJjbOVh50uQojtgU2SZK8H3qdx9kb7EFX473tM84OmX1m9d60oThRuRB_NkzFpo6FW9Hxr_iBPFMlUJn4SlhdZHNOMG9EjjLLO7RJHMGXTPZTv_-Fc7C7X9Z255EvmkQRb0SnL3qKlCvUrG2WR0DG_zgsY_WYTNBRYkOwjsOhbPWWsYZvwxiDoYYm9C2Bw'
# token_v = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IlRoaWFnbyIsInN1YiI6IjEzIiwianRpIjoiZDBlMGFkZDItOTlkMC00NWY1LThlYzEtY2FiYzIwZjkxMGYyIiwiaWF0IjoxNTAwMDMzMjE0LCJKd3RWYWxpZGF0aW9uIjoiVXN1YXJpbyIsIm5iZiI6MTUwMDAzMzIxMywiZXhwIjoxNTAwMDMzMjczLCJpc3MiOiJJc3N1ZXIiLCJhdWQiOiJBdWRpZW5jZSJ9.SmjuyXgloA2RUhIlAEetrQwfC0EhBmhu-xOMzyY3Y_Q'
