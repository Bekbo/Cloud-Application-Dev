import uuid
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from azure.cosmos import CosmosClient, PartitionKey
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import PIL.Image as Image
import io
from azure.storage.blob import BlobServiceClient, PublicAccess, ContentSettings, ContainerClient
endpoint = "https://lab5dbbekbolat.documents.azure.com:443/"
key = '8NapC9sReKX83uKVs7TpkctCZbQ3iYFH1yaMx2Lo3eOl0nHJ1iNEwtDaUpZOd3Li2Gpd1JJDtdda3B9IVT3Rpw=='
database_name = 'Test'
container_name = 'Pets'
sas = "https://lab5storagebekbolat.blob.core.windows.net/images?sp=racwdl&st=2021-03-11T18:07:43Z&se=2021-03-19T02:07:43Z&spr=https&sv=2020-02-10&sr=c&sig=2%2BB%2Ft9EE1OdMDfNTb6nuuiXUnf742Z2YI0N3s0EZ1zA%3D"


def push_image(picture, name, age, category):
    container = ContainerClient.from_container_url(sas)
    item_id = uuid.uuid1()
    blob_name = str(item_id) + '.' + picture.name.split('.')[1]
    pil_im = Image.open(picture)
    b = io.BytesIO()
    pil_im.save(b, 'jpeg')
    im_bytes = b.getvalue()
    container.upload_blob(name=blob_name, data=im_bytes)
    item_create = {
        'id': str(item_id),
        'name': name,
        'age': age,
        'category': category,
        'picture': 'https://lab5storagebekbolat.blob.core.windows.net/images/' + blob_name
    }
    return item_create


def push_item(item):
    pass


@csrf_exempt
def hello(request):
    context = {
        'items': [],
        'status_text': 'ok',
        'created': {}
    }
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/name"),
        offer_throughput=400
    )
    query = "SELECT * FROM c items"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    context['items'] = items
    if request.method == 'GET':
        return render(request, template_name='index.html', context=context)
    elif request.method == 'POST':
        picture = request.FILES.get('picture')
        item = push_image(picture, request.POST['name'], request.POST['age'], request.POST['category'])
        container.upsert_item(body=item)
        items.append(item)
        context['items'] = items
        return render(request, template_name='index.html', context=context)
    elif request.method == 'PUT':
        print(request.PUT)
        pass
    else:
        pass
    return render(request, template_name='index.html', context=context)


@csrf_exempt
def get_item(request, pk, name):
    context = {
        'item': [],
        'status_text': 'ok',
        'created': {}
    }
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/name"),
        offer_throughput=400
    )
    print(request)
    if request.method == "DELETE":
        print('delete')
        try:
            container.delete_item(item=pk, partition_key=name)
        except CosmosResourceNotFoundError:
            return HttpResponse("Resource not Found")
        return redirect('http://127.0.0.1:8000')
        # return render(request, template_name='index.html', context=context)
    elif request.method == 'POST':
        item = {
            'id': request.POST.get('id'),
            'name': request.POST.get('name'),
            'age': request.POST.get('age'),
            'category': request.POST.get('category'),
            'picture': request.POST.get('picture')
        }
        # picture = request.FILES.get('picture')
        # item = push_image(picture, request.POST['name'], request.POST['age'], request.POST['category'])
        container.replace_item(item=item['id'], body=item)
        context['item'] = [item]
        return render(request, template_name='index.html', context=context)
    else:
        item = container.read_item(pk, partition_key=name)
        context['item'] = item
    return render(request, template_name='index.html', context=context)
