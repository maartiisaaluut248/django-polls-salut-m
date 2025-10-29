from django.http import HttpResponse

def index(request):
    return HttpResponse("Hola, això és la pàgina de polls!")
