import logging
import azure.functions as func
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeServiceClient
from pandas import DataFrame
from docx import Document
from arcgis.gis import GIS

app = func.FunctionApp()

@app.route(route="GetMessage", auth_level=func.AuthLevel.ANONYMOUS)
def GetMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        filename = req.params.get('name')
        if not filename:
            return func.HttpResponse("Pass 'name' as a query string parameter.", status_code=400)
        
        doc = Document()
        doc.add_paragraph(req.get_body().decode('utf-8'))
        doc.save(f"{filename}.docx")

        SaveFile(filename)
                
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("An error occurred while processing the request.", status_code=500)
    
    return func.HttpResponse(f"File {filename}.docx created successfully.", status_code=200)

@app.route(route="GetGeographicLocation", auth_level=func.AuthLevel.ANONYMOUS)
def GetGeographicLocation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GeographicLocation HTTP trigger function processed a request.')

    try:
        gis = GIS(os.environ["ArcGISUsername"], os.environ["ArcGISPassword"])
        item = gis.content.search(req.get_body().decode('utf-8'), item_type="Feature Layer")[0]
        feature_layer = item.layers[0]
        features = feature_layer.query()
        df = DataFrame(features.sdf)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("An error occurred while processing the request.", status_code=500)
    
    return func.HttpResponse(df.to_json(), status_code=200)

def SaveFile(filename: str):
    managedIdentityCredential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url=os.environ["BlobStorageUrl"], credential=managedIdentityCredential)
    container_client = blob_service_client.get_container_client("output")
    blob_client = container_client.get_blob_client(f"{filename}.docx")
    with open(f"{filename}.docx", "rb") as data:
        blob_client.upload_blob(data)
