# ShareMon

This Azure Function is designed to monitor the contents of a particular folder on a regular basis.  When the function detects that there are files in the folder, it uploads them to a container in Azure Blob Storage and then deletes the source files.

This Function was built in order to workaround the issue that Azure Files does not trigger any events when it receives new files.

It is assumed that the source folder is one that has been mounted from an Azure Files Share.

# Design

This application is built using Azure Durable Functions and Python.  The Azure Function App is comprised of several functions.  They work together in order to monitor the input folder (Azure Files) and move data to the output container (Azure Blob Storage) as shown in the following diagram.  Azure Application Insights and Azure Log Analytics, also shown in the diagram) support the Function App by providng monitoring capabilities.

![Architecture Diagram](/bin/Flow.png)

Inside the Function App, there is a HTTP trigger that is responsible for starting the Orchestrator function.  This trigger has been hardcoded to a particular instance ID in order to force the orchestrator to run as a singleton.  When invoked, if the orchestrator hasn't already been started, this trigger will start it, then it will return a status page that includes links that may be used to check the orchestrator's status, stop it, etc..  

The Orchestrator function itself is an eternal function.  It employs two activity functions.  The first gathers a list of files from the source folder.  The second uploads and deletes them.  The Orchestrator is built to run 60 seconds after the uploading activity completes.  

![Function App Detail](/bin/Detail.png)

This implementation uses an eternal function approach instead of a timer approach because it's possible that the upload activity may take longer than a timer interval and the timer approach could result in overlapping executions with unexpected results.

# Configuration

The function app itself should have a Azure Files share added to it as described in the references, or in this [document](Prepare_app.md).

The function app also requires these configuration parameters:
- ShareMonSourceDirectory - path to the fileshare within the function app; example: /share01
- ShareMonDestinationConnectionString - a storage connection string to the desired blob storage account
- ShareMonDestinationContainerName - the name of the blob storage container that will receive the uploaded files

# Resources

This application was built using the following references:

- [Mount a File Share to a Function App](https://learn.microsoft.com/en-us/azure/azure-functions/scripts/functions-cli-mount-files-storage-linux)
- [Azure Durable Functions - Eternal Orchestration Example](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-eternal-orchestrations?tabs=python)
- [Azure Durable Functions - Singleton Example](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-singletons?tabs=python)
- [Azure Durable Functions - Fant Out Example](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-cloud-backup?tabs=python)