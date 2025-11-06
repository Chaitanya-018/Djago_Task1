from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

def sample(request):
    return HttpResponse('Hello world')

def sample1(request):
    return HttpResponse('welcome to django')

def sampleInfo(request):
    #data={"name":'Chaitanya',"age":25,"city":'hyd'} #json string
    #data=[4,6,8,9] #if we are trying to pass non dict objects we use parameter safe=False
    #return JsonResponse(data,safe=False)
    data={'result': [4,6,8,9]} #if we want pass list in dict
    return JsonResponse(data)


def dynamicResponse(request):
    name=request.GET.get("name",'')
    city=request.GET.get("city",'hyd')
    return HttpResponse(f"hello {name} from {city}")


def addition(request):
    num1 = request.GET.get("num1")
    num2 = request.GET.get("num2")
    # Convert to integers
    num1 = int(num1)
    num2 = int(num2)
    result = num1 + num2
    return HttpResponse(f"Addition = {result}")

def subtraction(request):
    num1 = request.GET.get("num1")
    num2 = request.GET.get("num2")

    num1 = int(num1)
    num2 = int(num2)

    result = num1 - num2
    return HttpResponse(f"Subtraction = {result}")


def multiplication(request):
    num1 = request.GET.get("num1")
    num2 = request.GET.get("num2")

    num1 = int(num1)
    num2 = int(num2)

    result = num1 * num2
    return HttpResponse(f"Multiplication = {result}")


def division(request):
    num1 = request.GET.get("num1")
    num2 = request.GET.get("num2")

    num1 = int(num1)
    num2 = int(num2)

    if num2 == 0:
        return HttpResponse("Error: Division by zero is not allowed")

    result = num1 / num2
    return HttpResponse(f"Division = {result}")

