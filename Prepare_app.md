This function is designed to periodically check the contents of a specifed directory and move these items to a Blob Storage Account.

It is assumed that the directory being monitored is an Azure Files Fileshare.  This fileshare should be added to the Function App that hosts this code using the technique described in this [article](https://learn.microsoft.com/en-us/azure/azure-functions/scripts/functions-cli-mount-files-storage-linux).

```Command Shell
SET RESOURCE_GROUP=<RESOURCE-GROUP>
SET FUNCTION_APP_NAME=<FUNCTION-APP-NAME>
SET SHARE_NAME=<SHARE-NAME>
SET STORAGE_ACCOUNT_NAME=<STORAGE-ACCOUNT-NAME>
SET MOUNT_PATH=<MOUNT-PATH>
SET STORAGE_ACCOUNT_KEY=<STORAGE-ACCOUNT-KEY>

az webapp config storage-account add ^
--resource-group %RESOURCE_GROUP% ^
--name %FUNCTION_APP_NAME% ^
--custom-id %SHARE_NAME% ^
--storage-type AzureFiles ^
--share-name %SHARE_NAME% ^
--account-name %STORAGE_ACCOUNT_NAME% ^
--mount-path %MOUNT_PATH% ^
--access-key %STORAGE_ACCOUNT_KEY%
```

Sample input:
```Command Shell
SET RESOURCE_GROUP=2023-09-12-RG-01
SET FUNCTION_APP_NAME=func4020
SET SHARE_NAME=share01
SET STORAGE_ACCOUNT_NAME=store4020
SET MOUNT_PATH=/share01
SET STORAGE_ACCOUNT_KEY=SECRET-OBTAINED-FROM-AZURE-PORTAL
```