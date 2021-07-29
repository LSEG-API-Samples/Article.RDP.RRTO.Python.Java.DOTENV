import os
import json
from dotenv import load_dotenv
import requests

if __name__ == '__main__':

    client_secret = ''
    scope = 'trapi'
    universe = '7203.T'

    load_dotenv()

    print(os.getenv('RTO_USER'))

    # RDP Login
    auth_endpoint = os.getenv('RDP_WS_AUTH_URL') 
    # -- Init and Authenticate Session
    auth_request_msg = {
        'username': os.getenv('RDP_USER') ,
	    'password': os.getenv('RDP_PASSWORD') ,
	    'grant_type': "password",
	    'scope': scope,
	    'takeExclusiveSignOnControl': "true"
    }
    
    try:
        response = requests.post(auth_endpoint, headers = {'Accept':'application/json'}, data = auth_request_msg, auth = (os.getenv('RDP_APP_KEY'), client_secret))
    except Exception as exp:
        print('Caught exception: %s' % str(exp))

    if response.status_code == 200:  # HTTP Status 'OK'
        print('Authentication success')
        auth_obj = response.json()
    else:
        print('RDP authentication result failure: %s %s' % (response.status_code, response.reason))
        print('Text: %s' % (response.text))

    # ESG Data
    esg_url = os.getenv('RDP_ESG_URP') 
    payload = {'universe': universe}

    try:
        response = requests.get(esg_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
    except Exception as exp:
        print('Caught exception: %s' % str(exp))

    if response.status_code == 200:  # HTTP Status 'OK'
        print('This is a ESG data result from RDP API Call')
        print(response.json())
        esg_object=response.json()
    else:
        print('RDP APIs: ESG data request failure: %s %s' % (response.status_code, response.reason))
        print('Text: %s' % (response.text))

    print('\n')

    

    # https://developers.refinitiv.com/en/article-catalog/article/using-rdp-api-request-esg-data-jupyter-notebook
    import pandas as pd
    import numpy as np
    headers=esg_object['headers']
    
    #Get column headers/titles using lambda
    titles=map(lambda header:header['title'], headers)
    
    dataArray=np.array(esg_object['data'])
    df=pd.DataFrame(data=dataArray,columns=titles)
    
    if df.empty is False:
        print(df)
