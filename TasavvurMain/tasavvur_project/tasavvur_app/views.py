from django.db.models import Q, Func, F
from django.http import JsonResponse
from django.shortcuts import render
from .models import DataSets

def base_part(request):
    return render(request, 'tasavvur_t/home.html')


def chat_bot(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        response = 'Salom, men sizning chatbot yordamchingizman'
        j_response = {'message': message_text, 'response': response}
        return JsonResponse(j_response)
    elif request.method == 'GET':
        file_name = request.GET.get('file_id')
        print(file_name)
        return render(request, 'tasavvur_t/chat.html')

    return render(request, 'tasavvur_t/chat.html')


def data_search(request):
    all_data = None
    if request.method == 'GET':
        search_text = request.GET['search_text']
        if len(search_text) == 0:
            all_data = DataSets.objects.all()
        else:
            all_data = DataSets.objects.filter(title__icontains=search_text)



    return render(request, 'tasavvur_t/data_search.html', context={'all_data': all_data})
