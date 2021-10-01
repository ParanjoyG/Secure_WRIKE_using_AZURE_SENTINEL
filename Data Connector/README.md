## **WRIKE AUDIT DATA CONNECTOR**

This is a Data Connector to log your Wrike Audit data into your Azure Sentinel Monitor.
You can deploy the connector in two ways :
* Using the ARM and Azure Function App.
* Manually using the files that are provided to you

Please make sure that you follow the instructions provided in the Data Connector page carefully.
Your data will be logged into the table `AuditLog_CL` .

Also make sure you have the correct subscription type in Wrike to generate the Audit Logs.
