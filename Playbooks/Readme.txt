Wrike-SendIncident_and_VirusTotalReport_viaEmail

Description- This Playbook automates the process of sending the Incident to the SOC analyst via email and also checks the associated IP address by querying Virustotal v3 IP Scan. This way the soc team can be up-to-date on the incidents occuring in the related wrike environment. 

Prerequisites:-

1. Deploy the Playbook using Custom Deployment. 
   a. Go to Azure Portal and create a resource. Within that search for Template Deployment(deploy using custom template)
   b. Create a resource using ARM and custom template. Click on "build your own template in the editor. 
   c. Paste the azuredeploy.json file contents and click save.
   d. Once done, fill in the necessary details and click "Review and Create" to create the logic app resource.
   e. After successful validation and deployment, you can use the playbook by following the next steps.

2. Create a OAuth2 client app in Google cloud platform and use the client ID and client Secret to enable the Gmail connector and use it with the Azure Sentinel connector. [Read](https://docs.microsoft.com/en-us/azure/connectors/connectors-google-data-security-privacy-policy). Also do not forget to give access to the client app for the google user whose account you will be using to call the Gmail API and send emails from. You can do this from the OAuth consent page after the creation of your app is complete. [Read-->](https://stackoverflow.com/questions/65756266/error-403-access-denied-the-developer-hasn-t-given-you-access-to-this-app-despi) 

3. To run the Playbook you must have the necessary sentinel and logic apps roles assigned to you.

Restrictions:-

1.This playbook only works with analytic rules provided with the Wrike solution and have IP as an entity type. 
