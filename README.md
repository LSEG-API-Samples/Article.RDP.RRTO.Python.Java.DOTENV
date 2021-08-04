# How to separate your credentials, secrets, and configurations from your source code with environment variables
- version: 1.0
- Last update: July 2021
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

## <a id="intro"></a>Introduction

As a modern application, your application always deal with credentials, secrets and configurations to connect to other services like Authentication service, Database, Cloud services, Microservice, ect. It is not a good idea to keep your username, password and other credentials hard code in your source code as your credentials may leak when you share or publish the application. You need to delete or remark those credentials before you share the code which adds extra work for you. And eventually, you may forgot to do it.

The services configurations such as API endpoint, Database URL should not be embedded in the source code too. The reason is every time you change or update the configurations you need to modify the code which may lead to more errors. 

How should we solve this issue?

## <a id=""></a>Store config in the environment

The [Twelve-Factor App methodology](https://12factor.net/) which is one of the most influential pattern to designing scalable software-as-a-service application. The methodology [3rd factor](https://12factor.net/config) (aka Config principle) states that configuration information should be kept as environment as environment variables and injected into the application on runtime as the following quotes:

>An app’s config is everything that is likely to vary between deploys (staging, production, developer environments, etc). This includes:
>- Resource handles to the database, Memcached, and other backing services
>- Credentials to external services such as Amazon S3 or Twitter
>- Per-deploy values such as the canonical hostname for the deploy
>
>Apps sometimes store config as constants in the code. This is a violation of twelve-factor, which requires strict separation of config from code. Config varies substantially across deploys, code does not.

>The twelve-factor app stores config in environment variables (often shortened to env vars or env). Env vars are easy to change between deploys without changing any code; unlike config files, there is little chance of them being checked into the code repo accidentally; and unlike custom config files, or other config mechanisms such as Java System Properties, they are a language- and OS-agnostic standard.

### What is Environment Variables?

An environment variable is a dynamic-named value that set through the Operating System, not the program. The variables are impact the process the OS and running process. In Widows, you can access the environment variables to view or modify them through This PC --> Properties --> Advanced system settings --> Environment Variables.. menu.

![Figure-1](images/01_windows_envs.png "Windows Environment Variables") 

The benefits of storing credentials and configurations in environment variables are the following:
1. The credentials and configurations are separated from the code. Project team can change the credentials and configurations based on scenario and environment (Dev, Test, Product, etc) without touching the application source code. 
2. The sensitive information (username, password, token, etc) are kept and maintain locally. The team can share the code among peers without be worried about information leak. 
3. Reduce the possibility of messing up between environments such as configure the Production server address in the Test environment.  

However, the environment variable has OS dependency. Each OS requires different way to access and modify the variables. It is not always practical to set environment variables on development machines (as the variables may keeps growing) or continuous integration servers where multiple projects are run.

These drawbacks leads to the *dotenv* method. 

## Introduction to .ENV file and dotenv

The dotenv method lets the application loads variables from a ```.env``` file into environment/running process the same way as the application load variables from environment variables. The application can load or modify the environment variables from the OS and ```.env``` file with a simple function call.

[dotenv](https://github.com/bkeepers/dotenv) is a library that originates from [Ruby](https://www.ruby-lang.org/en/) developers (especially the [Ruby on Rails](https://rubyonrails.org/) framework) and has been widely adopted and ported to many programming languages such as [python-dotenv](https://github.com/theskumar/python-dotenv), [dotenv-java](https://github.com/cdimascio/dotenv-java), [Node.js](https://github.com/motdotla/dotenv), etc. 

The ```.env``` file is a simple text file locates at the root of the project with a key-value pair setting as the following:

```
# DB
DB_USER=User
DB_PASSWORD=MyPassword
# Cloud
CLOUD_URL=192.168.1.1
```

Please note that you *do not* need the ```""``` or ```''``` characters for a string value.

### Caution

You *should not* share this ```.env``` file to your peers or commit/push it to the version control. You should add the file to the ```.gitignore``` file to avoid adding it to a version control or public repo accidentally.

You can create a ```.env.example``` file as a template for environment variables and ```.env``` file sharing. The file has the same parameters' keys as a ```.env``` file but without values as the following example:

```
# DB
DB_USER=
DB_PASSWORD=
# Cloud
CLOUD_URL=
```

Then you can push this ```.env.example``` file to the repository. Developers who got your source code project can create their own ```.env``` file from this template ```.env.example``` file. 

Please note that if the configuration is not a sensitive information (such as a public API endpoint URL), you can include it to a ```.env.example``` file. 

## dotenv with Python

Let's demonstrate with the [python-dotenv](https://github.com/theskumar/python-dotenv) library first. The example console application uses python-dotenv library to store the [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) credentials and configurations. 

### <a id="whatis_rdp"></a>What is Refinitiv Data Platform (RDP) APIs?

The [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) provide various Refinitiv data and content for developers via easy to use Web based API.

RDP APIs give developers seamless and holistic access to all of the Refinitiv content such as Historical Pricing, Environmental Social and Governance (ESG), News, Research, etc and commingled with their content, enriching, integrating, and distributing the data through a single interface, delivered wherever they need it.  The RDP APIs delivery mechanisms are the following:
* Request - Response: RESTful web service (HTTP GET, POST, PUT or DELETE) 
* Alert: delivery is a mechanism to receive asynchronous updates (alerts) to a subscription. 
* Bulks:  deliver substantial payloads, like the end of day pricing data for the whole venue. 
* Streaming: deliver real-time delivery of messages.

This example project is focusing on the Request-Response: RESTful web service delivery method only.  

For more detail regarding Refinitiv Data Platform, please see the following APIs resources: 
- [Quick Start](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/quick-start) page.
- [Tutorials](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials) page.
- [RDP APIs: Introduction to the Request-Response API](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api) page.
- [RDP APIs: Authorization - All about tokens](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens) page.

## python-dotenv and .env file set up

You can install the python-dotenv library via the following pip command:

```
pip install python-dotenv
```

The create a ```.env``` file at the root of the project with the following content

```
# RDP Core Credentials
RDP_USER=<Your RDP username>
RDP_PASSWORD=<Your RDP password>
RDP_APP_KEY=<Your RDP appkey>

# RDP Core Endpoints
RDP_BASE_URL = https://api.refinitiv.com
RDP_AUTH_URL=/auth/oauth2/v1/token
RDP_ESG_URL=/data/environmental-social-governance/v2/views/scores-full
```

## Using python-dotenv library

To use the python-dotenv library, you just import the library and call ```load_dotenv()``` statement. Then you can access both System environment variables and ```.env```'s configurations from the Python ```os.environ``` or ```os.getenv``` statement. 

Please note that the OS/System's environment variables always override ```.env``` configurations by default as the following example. 

```
import os
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

print('User: ', os.getenv('USERNAME')) # Return your System USERNAME configuration.
```

The following example shows how to use get configurations from a ```.env``` file to get the RDP APIs Auth service endpoint and user's RDP credential. 

```
# Get RDP Token service information from Environment Variables
base_URL = os.getenv('RDP_BASE_URL')
auth_endpoint = base_URL + os.getenv('RDP_AUTH_URL') 

# Get RDP Credentials information from Environment Variables
username = os.getenv('RDP_USER')
password = os.getenv('RDP_PASSWORD')
app_key = os.getenv('RDP_APP_KEY')
```

Next, the application creates the RDP Auth service request message and sends the HTTP Post request message to the RDP APIs endpoint.

```
import requests

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
```
The next step is requesting ESG (Environmental, Social, and Governance) data from RDP. We use the ESG scores-full API endpoint which provides full coverage of Refinitiv's proprietary ESG Scores with full history for consumers as an example API.

The ESG scores-full API requires the item name (aka universe) information which is most likely to be different for each individual run , so we get this information via a command line argument. 

```
import argparse

my_parser = argparse.ArgumentParser(description='Interested Symbol')
my_parser.add_argument('-i','--item', type = str, default= 'LSEG.L')
args = my_parser.parse_args()

universe = args.item
```

We get the RDP ESG Service API endpoint from a ```.env``` file.

```
# Get RDP Token service information from Environment Variables
esg_url = base_URL + os.getenv('RDP_ESG_URL') 

payload = {'universe': universe}
esg_object = None

# Request data for ESG Score Full Service
try:
    response = requests.get(esg_url, headers={'Authorization': 'Bearer {}'.format(auth_obj['access_token'])}, params = payload)
except Exception as exp:
    print('Caught exception: %s' % str(exp))
```
Then we can get the ESG data from the ```response.json()``` statement for further data processing.

The above code shows that you do not need to change the code if the RDP credentials or service endpoint is changed (example update API version). We can just update the configurations in a ```.env``` file and re-run the application.

## <a id="references"></a>References
For further details, please check out the following resources:
* [Refinitiv Data Platform APIs page](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) on the [Refinitiv Developer Community](https://developers.refinitiv.com/) website.
* [Refinitiv Data Platform APIs Playground page](https://api.refinitiv.com).
* [Refinitiv Data Platform APIs: Introduction to the Request-Response API](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api).
* [Refinitiv Data Platform APIs: Authorization - All about tokens](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens).
* [Using RDP API to request ESG data on Jupyter Notebook](https://developers.refinitiv.com/en/article-catalog/article/using-rdp-api-request-esg-data-jupyter-notebook)
* [python-dotenv GitHub page](https://github.com/theskumar/python-dotenv)
* [How to NOT embedded credential in Jupyter notebook](https://yuthakarn.medium.com/how-to-not-show-credential-in-jupyter-notebook-c349f9278466)
https://www.reddit.com/r/node/comments/6cz4jw/having_trouble_understanding_the_benefits_and/


For any questions related to Refinitiv Data Platform, please use the Developers Community [Q&A Forum](https://community.developers.refinitiv.com/spaces/231/index.html).