import logging
import azure.functions as func

app = func.FunctionApp()

@app.route(auth_level=func.AuthLevel.ANONYMOUS)
def GetMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        name = req.params.get('name') or req.get_json().get('name')
        if not name:
            return func.HttpResponse("Pass 'name' as a query string parameter.", status_code=400)
                        
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("An error occurred while processing the request.", status_code=500)
    
    return func.HttpResponse(f"Hello {name}", status_code=200)
