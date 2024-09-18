import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .config import oauth_secret, filters


class IndexView(LoginRequiredMixin, View):
    login_url = 'accounts/login/'  # Страница авторизации
    redirect_field_name = 'redirect_to'  # Поле, в которое будет передана ссылка после авторизации

    def get(self, request):  # Переход на главную страницу
        return render(request, 'index.html')

    def post(self, request):

        # Получение ссылки из формы (str)
        public_key: str = request.POST.get('public_key')

        # Получение фильтра из формы (str)
        filter: str = request.POST.get('filter')

        # Используем Yandex API для получения списка файлов с диска(json)
        url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
        headers = {f'Authorization': f'OAuth {oauth_secret}'}
        response = requests.get(url, headers=headers)

        # Получение списка файлов с диска из фильтра (list)
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

        # Получение списка файлов с диска без фильтра(list)
        else:
            files = response.json()['_embedded']['items']

        # Вывод списка файлов с диска
        context = {'files': files, 'public_key': public_key, 'filters': filters}
        return render(request, 'index.html', context)
