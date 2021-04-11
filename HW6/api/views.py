import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from msal import PublicClientApplication
# Create your views here.
from api.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from api.graph_helper import *


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error is not None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def sign_in(request):
    flow = get_sign_in_flow()
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    return HttpResponseRedirect(flow['auth_uri'])


def callback(request):
    # Make the token request
    result = get_token_from_code(request)
    # Get the user's profile
    user = get_user(result['access_token'])
    # Store user
    store_user(request, user)
    return HttpResponseRedirect(reverse('home'))


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))


def index(request):
    app = PublicClientApplication(client_id="9f2ec1b4-8280-459e-846a-22942d623331",
                                  authority="https://login.microsoftonline.com/57081b5e-e66a-4993-8eaf-15b0b309293f")
    scopes = ["User.Read"]
    flow = app.initiate_device_flow(scopes=scopes)
    context = {
        'code': flow['user_code'],
        'user': ''
    }
    return render(request, 'index.html', context=context)
    # print(flow)
    # res = app.acquire_token_by_device_flow(flow=flow)
    # print(res['id_token_claims'])

    # payload = {'client_id': '9f2ec1b4-8280-459e-846a-22942d623331', 'response_type': 'code', 'response_mode': 'query',
    #            }
    # get_authorization_code = requests.get('https://login.microsoftonline.com/57081b5e-e66a-4993-8eaf-15b0b309293f/oauth2/authorize',
    #                                       params=payload, verify=False)
    # return HttpResponse(get_authorization_code)
    return HttpResponse(res)


def main(request):
    context = initialize_context(request)
    return render(request, 'index.html', context)
