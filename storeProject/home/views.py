from django.shortcuts import render
from django.views import View


# Create your views here.


class Hoem(View):
    def get(self, request):
        return render(request, 'home.html')
