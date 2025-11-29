from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew, InstaPost
from basic.models import Users
from django.contrib.auth.hashers import make_password,check_password

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

#to test database connection through api
def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})
    
@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method == 'POST':
        data=json.loads(request.body)
        student=StudentNew.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
            )
        return JsonResponse({"status":"success","id":student.id},status=200)
    #return JsonResponse({"error":"use post method"},status=400)

    elif request.method=="GET":
        result=list(StudentNew.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)


    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        new_email=data.get("email") #getting email
        existing_student=StudentNew.objects.get(id=ref_id) #fetched the object as per the id
        existing_student.email=new_email #updating with new email
        existing_student.save()
        updated_data=StudentNew.objects.filter(id=ref_id).values().first()        
        return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)


    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        get_delting_data=StudentNew.objects.filter(id=ref_id).values().first()
        to_be_delete=StudentNew.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"status":"success","message":"student record deleted successfully","deleted data":get_delting_data},status=200)
    return JsonResponse({"error":"use post method"},status=400)

#task insta post
@csrf_exempt
def addPost(request):
    print(request.method)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = InstaPost.objects.create(
                post_name=data.get('post_name'),
                post_type=data.get('post_type'),
                post_date=data.get('post_date'),
                post_description=data.get('post_description')
            )
            return JsonResponse({
                "status": "success","id": post.id,"message": "Post created successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Use POST method only"}, status=405)

#ORM methods Task
def orm_operations(request):
    #1.Get all records
    all_students = list(StudentNew.objects.values())

    #2.Get specific record by id
    specific_student = StudentNew.objects.filter(id=1).values().first()

    #3.Filter by age >= 20
    age_gte_20 = list(StudentNew.objects.filter(age__gte=20).values())

    #4.Count total students
    age_lte_25 = list(StudentNew.objects.filter(age__lte=25).values())

    #5.Order by name
    ordered_by_name = list(StudentNew.objects.order_by('name').values())

    #6.Get unique ages
    unique_ages = list(StudentNew.objects.values_list('age', flat=True).distinct())

    #7.Count total students
    total_students = StudentNew.objects.count()

    data = {
        "all_students": all_students,
        "specific_student": specific_student,
        "age_gte_20": age_gte_20,
        "age_lte_25": age_lte_25,
        "ordered_by_name": ordered_by_name,
        "unique_ages": unique_ages,
        "total_students": total_students
    }
    return JsonResponse(data, safe=False)

def job1(request):
    return JsonResponse({"message":"u have successfully applied for job1"},status=200) 
def job2(request):
    return JsonResponse({"message":"u have successfully applied for job2"},status=200)


# @csrf_exempt
# def signUp(request):
#     if request.method=="POST":
#         data=json.loads(request.body)
#         print(data)
#         user=Users.objects.create(
#             username=data.get("username"),
#             email=data.get("email"),
#             password=data.get("password")
#             )
#         return JsonResponse({"status":'success'},status=200)

@csrf_exempt
def signUp(request):
    if request.method=="POST":
        data=json.loads(request.body)
        print(data)
        user=Users.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            password=make_password(data.get("password"))
            )
        return JsonResponse({"status":'success'},status=200)

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = request.POST   #in postman use form
        print(data)
        username = data.get("username")
        password = data.get("password")
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                return JsonResponse(
                    {"status": "success", "message": "successfully logged in"},
                    status=200
                )
            else:
                return JsonResponse(
                    {"status": "failure", "message": "invalid password"},
                    status=400
                )

        except Users.DoesNotExist:
            return JsonResponse(
                {"status": "failure", "message": "user not found"},
                status=400
            )

    




    
# @csrf_exempt
# def check(request):
#     ipdata=request.POST
#     print(ipdata)
#     hashed=make_password(ipdata.get("ip"))
#     print(hashed)
#     return JsonResponse({"status":"success","data":hashed},status=200) 
# 

@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$870000$QFdX4auSTeBp9ptDBK8VU6$AYXfvB+2WYIc0MxVCS4e3SqGkijsX5tTUtSS3BvC08Q="
    ipdata=request.POST
    print(ipdata)
    # hashed=make_password(ipdata.get("ip"))
    x=check_password(ipdata.get("ip"),hashed)
    print(x)
    return JsonResponse({"status":"success","data":hashed},status=200)   