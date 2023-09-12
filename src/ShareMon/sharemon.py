import azure.functions as func
import azure.durable_functions as df
import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from pathlib import Path
from typing import List
from datetime import timedelta

bp = df.Blueprint()

#
# Orchestrator
#
@bp.orchestration_trigger(context_name="context")
def orchestrator(context: df.DurableOrchestrationContext):
    
    source_directory = os.environ["ShareMonSourceDirectory"]
    files = yield context.call_activity("GetFileList", source_directory)

    tasks = []
    for file in files:
        tasks.append(context.call_activity("CopyFileToBlob", file))
    results = yield context.task_all(tasks)

    next_iteration = context.current_utc_datetime + timedelta(seconds = 60)
    yield context.create_timer(next_iteration)

    context.continue_as_new(None)


#
# GetFileList
#
@bp.activity_trigger(activity="GetFileList", input_name="directory")
def GetFileList(directory: str) -> List[str]:

    files = []
    for file in Path(directory).iterdir():
        if (file.is_file):
            files.append(str(file))

    return files    

#
# CopyFileToBlob
#
@bp.activity_trigger(activity="CopyFileToBlob", input_name="source")
def CopyFileToBlob(source: str) -> str:

    connection_string = os.environ["ShareMonDestinationConnectionString"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = os.environ["ShareMonDestinationContainerName"]
    try:
        blob_service_client.create_container(container_name)
    except ResourceExistsError:
        pass

    file_name = Path(source).parts[-1]
    blob_name = file_name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    byte_count = os.path.getsize(source)

    with open(source, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    os.remove(source)

    return byte_count