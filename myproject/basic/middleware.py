from django.http import JsonResponse
import json
import re
from basic.models import Users

class basicMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    # def __call__(self,request):    #global middle for every view
    #     print(request,"hello")
    #     print(request.method,"method")
    #     print(request.path)
    #     response = self.get_response(request)
    #     return response

    
    def __call__(self,request):
        #print(request,"hello")
        if(request.path=="/student/"):
            print(request.method,"method")
            print(request.path)
        response = self.get_response(request)
        return response    
    

# class signupMiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response

#     def __call__(self,request):
#         data=json.loads(request.body)
#         username=data.get("username")
#         email=data.get("email")
#         dob=data.get("dob")
#         password=data.get("pswd")


class SscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=request.GET.get("ssc")
            #print(ssc_result,'hello')
            if(ssc_result !='True'):
                return  JsonResponse({"error":"u should qualify atleast ssc for applying this job"},status=400)
        return self.get_response(request)

 
class MedicalFitMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path == "/job1/"):
            medical_fit_result=request.GET.get("medically_fit")
            if(medical_fit_result !='True'):
                return JsonResponse({"error":"u not medically fit to apply for this job role"},status=400)
        return self.get_response(request)
 
class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path in ["/job1/","/job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if(Age_checker >25 and Age_checker<18):
                return JsonResponse({"error":"age must be in b/w 18 and 25"},status=400)
        return self.get_response(request)
    

class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path == "/signup/"):
            data=json.loads(request.body)
            username=data.get("username","")
            #checks username is empty or not
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            #checks length    
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should contains 3 to 20 characters"},status=400)
            #checks starting and ending
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not starts or ends with . or _"},status=400) 
            #checks allowed characters
            if not re.match(r"^[a-zA-Z0-9._]+$",username):
                return JsonResponse({"error":"username  should contains letters,numbers,dot,underscore"},status=400)
            #checks .. and  __
            if ".." in username or "__" in username:
                return JsonResponse({"error:cannot have .. or __"},status=400)   
        return self.get_response(request) 
       
class EmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/signup/":
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            email = data.get("email", "").strip()  #strip method removes spaces from starting and ending

            # 1. Check empty
            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            # 2. No spaces allowed
            if " " in email:
                return JsonResponse({"error": "Email should not contain spaces"}, status=400)

            # 3. Basic pattern validation
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, email):
                return JsonResponse({"error": "Enter a valid email format"}, status=400)

            # 4. Must contain @ + valid domain
            if "@" not in email:
                return JsonResponse({"error": "Email must contain '@' symbol"}, status=400)

            local, domain = email.split("@", 1)
            if not local or not domain:
                return JsonResponse({"error": "Email must have a valid username and domain"}, status=400)

            if "." not in domain:
                return JsonResponse({"error": "Email domain must contain a dot (.)"}, status=400)

            # 5. Unique (case-insensitive)
            if Users.objects.filter(email__iexact=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

        return self.get_response(request)   

class PasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/signup/":
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            username = data.get("username", "")
            email = data.get("email", "").strip()
            password = data.get("password", "")

            # 1. Minimum length 6
            if len(password) < 6:
                return JsonResponse({"error": "Password must be at least 6 characters long"}, status=400)

            # 2. Must contain lowercase
            if not re.search(r"[a-z]", password):   #Run this code if value is empty or false.
                return JsonResponse({"error": "Password must contain at least one lowercase letter"}, status=400)

            # 3. Must contain digits
            if not re.search(r"\d", password):  # \d = digit
                return JsonResponse({"error": "Password must contain at least one number"}, status=400)

            # 4. Should not be same as username
            if password.lower() == username.lower():
                return JsonResponse({"error": "Password should not be the same as username"}, status=400)

            # 5. Should not be same as email
            if password.lower() == email.lower():
                return JsonResponse({"error": "Password should not be the same as email"}, status=400)

            # 6. Should not be too weak (common bad passwords)
            weak_passwords = [
                "123456", "12345678", "123456789", "password", "qwerty",
                "abc123", "111111", "iloveyou", "admin", "welcome"
            ]

            if password.lower() in weak_passwords:
                return JsonResponse({"error": "Password is too weak. Choose a stronger password."}, status=400)

        return self.get_response(request)        

 


    




    

