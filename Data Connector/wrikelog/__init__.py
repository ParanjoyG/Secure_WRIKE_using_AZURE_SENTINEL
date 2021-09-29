import datetime
import logging
import json
import requests
import datetime
import hashlib
import hmac
import base64
import sys
import re
import os
import azure.functions as func
from .TimeKeeper import TimeManager


shared_key = os.environ['WorkspaceKey']
customer_id = os.environ['WorkspaceID']
access_token = os.environ['WrikeAccessToken']
connection_string = os.environ['AzureWebJobsStorage']
data_audits = 'NIL '



def show_error_message():
    path = os.path.abspath('details.txt')
    logging.info('\nIt seems you have encountered an error.\nIf you wanna change your Wrike or Azure Sentinel details, you can do so in \'details.txt\' located at '+path)

def fetch_data(date) :
    head = {
        "Authorization": "bearer {}".format(access_token)
    }
    URL_audit_log = 'https://www.wrike.com/api/v4/audit_log?eventDate={\"start\":\"'+date+'\"}'
    payload = {}
    try :
        resp = requests.request("GET", URL_audit_log,headers=head,data = payload)
        data_audits = json.dumps(json.loads(resp.content), indent=3)
        if resp.status_code >=200 and resp.status_code<=299 :
            data_length = len(json.loads(data_audits)['data'])
            logging.info("Audit Log Recieved.\n Size of Data : {}".format(data_length))
            if data_length == 0 :
                logging.info("Data not Logged due to being empty.")
                return [1]
            else :
                return [0, data_audits]
        elif resp.status_code == 403 :
            logging.error("The Wrike Access Token does not have authorised access.")
            show_error_message()
            return [1]
        elif resp.status_code == 401 :
            logging.error("Invalid Wrike Access Token.")
            show_error_message()
            return [1]
        else :
            logging.error("Error generated while fetching the data from Wrike with response code : {}".format(resp.status_code)) 
            show_error_message()
            return [1]
    except Exception as err :
        logging.error("Something went wrong. The Error states : {}".format(err)) 
        show_error_message()
        return [1]



def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")  
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
    return authorization

def post_data(customer_id, shared_key, body, log_type):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    try :
        response = requests.post(uri,data=body, headers=headers)
        if (response.status_code >= 200 and response.status_code <= 299):
            logging.info('Accepted')
            return [0]
        elif response.status_code == 403 :
            logging.error("Invalid Shared Key or Client ID of your Sentinel account")
            show_error_message()
            return [1]
        else :
            logging.error("Error generated while logging Data to Sentinel with response code : {}".format(response.status_code)) 
            show_error_message()
            return [1]
    except Exception as err :
        logging.error("Something went wrong. The Error states : {}".format(err))
        show_error_message()
        return [1]

def main(mytimer: func.TimerRequest) -> None:
    # utc_timestamp = datetime.datetime.utcnow().replace(
    #     tzinfo=datetime.timezone.utc).isoformat()

    # if mytimer.past_due:
    #     logging.info('The timer is past due!')

    # logging.info('Python timer trigger function ran at %s', utc_timestamp)

    logging.info('Shared Key is {}'.format(shared_key))
    logging.info('Customer Id is {}'.format(customer_id))
    time = TimeManager(connection_string=connection_string)
    log_time = time.get()
    if log_time == None :
        log_time = '2021-09-08T12:39:11Z\''
        log_time = log_time[:-1]
    fetch_status = fetch_data(log_time)
    if fetch_status[0] == 0 :
        data = json.loads(fetch_status[1])
        log_type = data["kind"]
        body = json.dumps(data["data"])
        post_status = post_data(customer_id, shared_key, body, log_type)
        log_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        time.post(log_time)
    if fetch_status[0]==1 or post_status[0]==1 :
        logging.error('Task Failed.')