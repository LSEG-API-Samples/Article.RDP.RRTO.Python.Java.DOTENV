import os
import json
import sys
import argparse
from dotenv import load_dotenv
import requests

if __name__ == '__main__':

    # Load Environment Variables
    load_dotenv()

    print('User: ', os.getenv('USERNAME'))

    # Build and Parse Command line arguments for item/universe, which always change.
    my_parser = argparse.ArgumentParser(description='Interested Symbol')
    my_parser.add_argument('-i','--item', type = str, default= 'LSEG.L')
    args = my_parser.parse_args()

    universe = args.item

    client_secret = ''
    scope = 'trapi'
    auth_obj = None

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
	    'password': password ,
	    'grant_type': "password",
	    'scope': scope,
	    'takeExclusiveSignOnControl': "true"
    }
    
    # Authentication with RDP Auth Service
    try:
        response = requests.post(auth_endpoint, headers = {'Accept':'application/json'}, data = auth_request_msg, auth = (app_key, client_secret))
    except Exception as exp:
        print('Caught exception: %s' % str(exp))

    if response.status_code == 200:  # HTTP Status 'OK'
        print('Authentication success')
        auth_obj = response.json()
    else:
        print('RDP authentication result failure: %s %s' % (response.status_code, response.reason))
        print('Text: %s' % (response.text))
    
    # If authentication fail, exit program.
    if auth_obj is None:
        print('Authentication fail, exit program')
        sys.exit(0)

    # Get RDP Token service information from Environment Variables
    esg_url = base_URL + os.getenv('RDP_ESG_URL') 

    payload = {'universe': universe}
    esg_object = None

    # Request data for ESG Score Full Service
    try:
        response = requests.get(esg_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
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

    # If ESG Data available, convert data to Pandas DataFrame
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
            print('Top 10 rows data is \n',df.head(10))
