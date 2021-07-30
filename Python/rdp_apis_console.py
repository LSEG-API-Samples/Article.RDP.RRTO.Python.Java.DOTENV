import os
import json
import sys
from dotenv import load_dotenv
from icecream import ic 
import requests

if __name__ == '__main__':

    client_secret = ''
    scope = 'trapi'
    universe = '7203.T'
    auth_obj = None

    load_dotenv()

    # Get RDP Token service information from Environment Variables
    base_URL = os.getenv('RDP_BASE_URL')
    auth_endpoint = base_URL + os.getenv('RDP_AUTH_URL') 

     # Get RDP Credentials information from Environment Variables
    username = os.getenv('RDP_USER')
    password = os.getenv('RDP_PASSWORD')
    app_key = os.getenv('RDP_APP_KEY')

    # -- Init and Authenticate Session
    auth_request_msg = {
        'username': username ,
	    'password': 'password' ,
	    'grant_type': "password",
	    'scope': scope,
	    'takeExclusiveSignOnControl': "true"
    }
    
    try:
        response = requests.post(auth_endpoint, headers = {'Accept':'application/json'}, data = auth_request_msg, auth = (app_key, client_secret))
    except Exception as exp:
        ic('Caught exception: %s' % str(exp))

    if response.status_code == 200:  # HTTP Status 'OK'
        print('Authentication success')
        auth_obj = response.json()
    else:
        print('RDP authentication result failure: %s %s' % (response.status_code, response.reason))
        print('Text: %s' % (response.text))
    
    if auth_obj is None:
        print('Authentication fail, exit program')
        sys.exit(0)

    # Get RDP Token service information from Environment Variables
    esg_url = base_URL + os.getenv('RDP_ESG_URL') 

    payload = {'universe': universe}
    esg_object = None
    try:
        response = requests.get(esg_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['refresh_token'])}, params = payload)
    except Exception as exp:
        print('Caught exception: %s' % str(exp))

    if response.status_code == 200:  # HTTP Status 'OK'
        print('Receive ESG Data from RDP, transform data to Pandas Dataframe format')
        #print(response.json())
        esg_object=response.json()
    else:
        print('RDP APIs: ESG data request failure: %s %s' % (response.status_code, response.reason))
        print('Text: %s' % (response.text))

    print('\n')

    if esg_object is not None:
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
