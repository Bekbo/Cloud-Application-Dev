from django.shortcuts import render
from azure.cosmos import CosmosClient, PartitionKey
from django.views.decorators.csrf import csrf_exempt
import shortuuid
endpoint = "https://hw9.documents.azure.com:443/"
key = '45URqHvvlOmmlfd5Y8NZnCVUqzA8IPYS4cGjSG2uSDQ9ngzhIFdrahkagNYWFwREIj1TXxFjYKtG6Rcjli1g5g=='
database_name = 'hw9'
container_name = 'Texts'
# Create your views here.


def index(request):
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    query = "SELECT t.text FROM Texts t"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    context = {
        'items': items
    }
    return render(request, template_name='index.html', context=context)


@csrf_exempt
def insert(request):
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    if request.method == 'POST':
        item = {
            "id": shortuuid.uuid(),
            "text": request.POST['text']
        }
        container.upsert_item(body=item)
    query = "SELECT t.text FROM Texts t"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    context = {
        'items': items
    }
    return render(request, template_name='index.html', context=context)
