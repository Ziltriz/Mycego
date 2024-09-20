import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .config import oauth_secret, filters


class IndexView(LoginRequiredMixin, View):
    login_url = 'accounts/login/'  # Login page URL
    redirect_field_name = 'redirect_to'

    def get(self, request):  # Redirect to a success page
        return render(request, 'index.html')

    def post(self, request):

        # Url from form (str)
        public_key: str = request.POST.get('public_key')

        # Filter from form(str)
        filter: str = request.POST.get('filter')

        # Get files from Yandex API(json)
        url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
        headers = {f'Authorization': f'OAuth {oauth_secret}'}
        response = requests.get(url, headers=headers)

        # Filter files (list)
        if filter is not None:
            filtered_files = []
            f = filter[:-1]
            media_type = filters[f]
            files = response.json()['_embedded']['items']
            for file in files:
                if file['media_type'] == media_type:
                    filtered_files.append(file)

            context = {'files': filtered_files, 'public_key': public_key, 'filters': filters}
            return render(request, 'index.html', context)

        # Files without filter(list)
        else:
            files = response.json()['_embedded']['items']

        # Render files
        context = {'files': files, 'public_key': public_key, 'filters': filters}
        return render(request, 'index.html', context)
