import requests
from django.shortcuts import render
from django.views import View
from .config import oauth_secret


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        public_key = request.POST.get('public_key')
        url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
        headers = {f'Authorization': f'OAuth {oauth_secret}'}
        response = requests.get(url, headers=headers)
        files = response.json()['_embedded']['items']
        context = {'files': files, 'public_key': public_key}
        return render(request, 'index.html', context)


def download_file(request, public_key, file_path):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_key}&path={file_path}'
    headers = {f'Authorization': f'OAuth {oauth_secret}'}
    file = requests.get(url, headers=headers).json()['href']
    response = requests.get(file)
    return response
