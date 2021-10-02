# Secure WRIKE using AZURE SENTINEL

Wrike is a product managemnet software, widely used in various industries like Health Care, Information Technology and even Finance. It is one of the top rated PMS with excellent security handling. To bolster its security even more we have a custom solution to monitor the various activities happening within the Wrike environment using Azure Sentinel. With the variety of contents provided, we can have a bird's eye view as well as a granular control over Wrike security.

# Inspiration

Wrike is not just restricted to one sector instead it has users from Siemens, Walmart, Capgemini, Nickelodeon, Sony Pictures and many more. Now along with the capabilities of **Azure Sentinel** we can provide a much more in-depth security analysis and overview to the SOC team.

# What it does?

One of the beautiful features of Azure Sentinel is its ability to ingest different types of logs using multiple methods and the integration of Sentinel along with Azure Defender gives a cross-domain view within the cloud environment. Our project consists of  :
* Log Agent
* Analytic Rules
* Threat Hunting Queries
* Parser
* Playbook
* Workbook

# Project Architechture

![Project Architecture](https://github.com/ParanjoyG/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/architechture.png)

# Steps for generating Wrike API Key

* Open your Wrike Workspace
* Go to `Apps & Integrations` at the top-right of your workspace
![Step 1](https://github.com/ParanjoyG/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Step%201.jpg)
* Then go to `API` at the top-left of your screen.
![Step 2](https://github.com/ParanjoyG/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Step%202.jpg)
* Enter an API name and then click on `Create`.
* Open your App and the scroll down to Create Token.
![Step 3](https://github.com/ParanjoyG/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Step%203.jpg)
* Enter your Wrike workspace password.
* Then click on `Copy Token` to copy the Permanent Access Token for further use.
![Step 4](https://github.com/ParanjoyG/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Step%204.jpg)

# Steps to log data into Azure Sentinel 

* Create your Azure Sentinel Workspace and then obtain the WORKSPACEID and PRIMARY/SECONDARY KEY.
* Clone the git repository in your local computer.\
`git clone https://github.com/ParanjoyG/Secure_WRIKE_using_AZURE_SENTINEL.git`
* Go to the follwing path \
`.../Secure_Wrike_using_AZURE_SENTINEL/DataConnector_Manual/`
* Install the required dependencies\
`pip install requirements.txt`
* Run the program `complete.py`
* Provide the required inputs - WorksspaceID, Primary Key, Wrike Access Token
* Your data will be logged in a custom log table with the name `AuditLog_CL`

