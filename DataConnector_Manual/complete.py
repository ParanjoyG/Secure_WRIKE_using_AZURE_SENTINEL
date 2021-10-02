import json
import requests
import datetime
import hashlib
import hmac
import base64
import sys
import re
import os

access_tok = ''
customer_id = ''
shared_key = ''

file = open('info.txt', 'r')
data = json.loads(file.read())
file.close()
date = data['time']

if os.path.exists('config.txt') :
    file = open('config.txt', 'r')
    config = json.loads(file.read())
    file.close()
    access_tok = config["Wrike API Access Token"]
    customer_id = config["Azure Sentinel Workspace ID"]
    shared_key = config["Azure Sentinel Workspace Key"]
else :
    access_tok = input("Enter Wrike API Permanent Access Token : ")
    customer_id = input("Enter Azure Sentinel Workspace ID : ")
    shared_key = input("Enter Primary/Secondary Key of your Azure Sentinel Workspace : ")
    configurations = {}
    configurations["Wrike API Access Token"] = access_tok
    configurations["Azure Sentinel Workspace ID"] = customer_id 
    configurations["Azure Sentinel Workspace Key"] = shared_key
    file = open('config.txt', 'w')
    config = file.write(json.dumps(configurations, indent=3))
    file.close()


def show_error_message():
    path = os.path.abspath('config.txt')
    print('\nIt seems you have encountered an error.\nIf you wanna change your Wrike or Azure Sentinel details, you can do so in \'config.txt\' located at '+path)


head = {
    "Authorization": "bearer {}".format(access_tok)
}
URL_audit_log = 'https://www.wrike.com/api/v4/audit_log?eventDate={\"start\":\"'+date+'\"}'

payload = {}


try :
    resp = requests.request("GET", URL_audit_log,headers=head,data = payload)
    data_audits = json.dumps(json.loads(resp.content), indent=3)
    if resp.status_code >=200 and resp.status_code<=299 :
        data_length = len(json.loads(data_audits)['data'])
        print("Audit Log Recieved.\nSize of data : {}".format(data_length))
        if data_length == 0 :
            print("Data not Logged due to being empty.")
    elif resp.status_code == 403 :
        print("The Wrike Access Token does not have authorised access.")
        show_error_message()
        sys.exit()
    elif resp.status_code == 401 :
        print("Invalid Wrike Access Token.")
        show_error_message()
        sys.exit()
    else :
        print("Error generated while fetching the data from Wrike with response code : {}".format(resp.status_code)) 
        show_error_message()
        sys.exit()
except Exception as err :
    print ("Something went wrong. The Error states : {}".format(err)) 
    show_error_message()
    sys.exit()


data['time'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
file = open('info.txt', 'w')
file.write(json.dumps(data))
file.close()

data = json.loads(data_audits)
log_type = data["kind"]
body = json.dumps(data["data"])

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
            print('Accepted')
        elif response.status_code == 403 :
            print("Invalid Shared Key or Client ID of your Sentinel account")
            show_error_message()
            sys.exit()
        else :
            print("Error generated while logging Data to Sentinel with response code : {}".format(response.status_code)) 
            show_error_message()
            sys.exit()
    except Exception as err :
        if re.search("Max retries exceeded",str(err)) :
            print("Maximum retries exceeded. Maybe the Client Id of your Azure account is Invalid.")
            show_error_message()
        else :
            print ("Something went wrong. The Error states : {}".format(err))
            show_error_message()
        sys.exit() 

if data_length > 0 :
    post_data(customer_id, shared_key, body, log_type)
