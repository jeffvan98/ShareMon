import azure.functions as func
import azure.durable_functions as df
from sharemon import bp

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app.register_blueprint(bp)

# 16772ca0-eedb-4483-acb2-9bc767d38d98

@app.route(route="HttpTrigger")
@app.durable_client_input(client_name="client")
async def HttpTrigger(req: func.HttpRequest, client) -> func.HttpResponse:
    instance_id = "16772ca0-eedb-4483-acb2-9bc767d38d98"
    existing_instance = await client.get_status(instance_id)
    if existing_instance.runtime_status in [df.OrchestrationRuntimeStatus.Completed, df.OrchestrationRuntimeStatus.Failed, df.OrchestrationRuntimeStatus.Terminated, None]:
        instance_id = await client.start_new("orchestrator", instance_id)

    return client.create_check_status_response(req, instance_id)
1