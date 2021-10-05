## **WRIKE AUDIT DATA CONNECTOR**

This is a Data Connector to log your Wrike Audit data into your Azure Sentinel Monitor.
You can deploy the connector in two ways :
* Using the ARM and Azure Function App.
* Manually using the files that are provided to you

Please make sure that you follow the instructions provided in the Data Connector page carefully.Here are some screenshots to give you a peek.

![Img1](https://github.com/HelloGit-ty/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Data%20Connector%20Instruction%20images/Image%201.png)

![Img2](https://github.com/HelloGit-ty/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Data%20Connector%20Instruction%20images/Image%202.png)

![Img3](https://github.com/HelloGit-ty/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Data%20Connector%20Instruction%20images/Image%203.png)

![Img4](https://github.com/HelloGit-ty/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Data%20Connector%20Instruction%20images/Image%204.png)

![Img5](https://github.com/HelloGit-ty/Secure_WRIKE_using_AZURE_SENTINEL/blob/main/Project%20Images/Data%20Connector%20Instruction%20images/Image%205.png)

Your data will be logged into the table `AuditLog_CL` .

## **FEW HEADS UP** 

1. Make sure you have the correct subscription type in Wrike to generate the Audit Logs.
2. This data connector is a API data connector type. Unlike the syslog data connector type we cannot ingest logs in real-time as they are being generated. Instead we can ingest them after a certain interval. **THIS IS WHY IT IS RECOMMENDED TO EXECUTE THIS DATA CONNECTOR AFTER A FIXED TIME INTERVAL (For instance once every hour or once every 2 hours or even once every 30 mins, as per your need)** 
3. Remember that there are a fixed number of REST calls you can make to the Wrike's API in a day and if you exceed that limit the data connector will not get anymore logs for that day. **HENCE IT'S ADVISABLE THAT YOU DO NOT RUN THE DATA CONNECTOR SO FREQUENTLY AS TO EXCEED THAT CALL LIMIT.** The call limit is set by Wrike and is applicable to all API based data connectors!
