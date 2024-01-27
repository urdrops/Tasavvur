from django.http import JsonResponse
from django.shortcuts import render


def base_part(request):
    return render(request, 'tasavvur_t/home.html')


def chat_bot(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        response = 'Hi, I am OpenAI Assistant'
        j_response = {'message': message_text, 'response': response}
        return JsonResponse(j_response)

    return render(request, 'tasavvur_t/chat.html')


def data_search(request):
    if request.method == 'GET':
        print(request.GET['search_text'])
    return render(request, 'tasavvur_t/data_search.html')
