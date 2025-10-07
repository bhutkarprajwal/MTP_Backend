from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view

@csrf_exempt
def register(request):
    if request.method=='POST':
        data=json.loads(request.body)
        username=data.get('username')
        email=data.get('email')
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        mobile_number=data.get('mobile_number')
        password=data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if User.objects.filter(mobile_number=mobile_number).exists():
            return JsonResponse({'error': 'Mobile number already exists'}, status=400)

        hashed_password = make_password(password)
        user=User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            password=hashed_password
        )
        user.save()
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

        if not check_password(password, user.password):
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

        # Send all user details except password
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile_number': user.mobile_number,
        }

        return JsonResponse({'message': 'Login successful', 'user': user_data}, status=200)

    return JsonResponse({'error': 'POST request required'}, status=400)
 


@csrf_exempt
def update_profile(request, user_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

    # Update fields if provided
    updated_fields = []

    if 'first_name' in data:
        user.first_name = data['first_name']
        updated_fields.append('first_name')

    if 'last_name' in data:
        user.last_name = data['last_name']
        updated_fields.append('last_name')

    if 'email' in data:
        try:
            validate_email(data['email'])
            user.email = data['email']
            updated_fields.append('email')
        except ValidationError:
            return JsonResponse({'error': 'Invalid email format'}, status=400)

    if 'mobile_number' in data:
        user.mobile_number = data['mobile_number']
        updated_fields.append('mobile_number')

    if 'password' in data:
        user.password = make_password(data['password'])
        updated_fields.append('password')

    if updated_fields:
        user.save(update_fields=updated_fields)

    return JsonResponse({
        'message': 'Profile updated successfully',
        'updated_fields': updated_fields,
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile_number': user.mobile_number
        }
    }, status=200)
    
@csrf_exempt
@api_view(['POST'])
def show_places(request):
    user_id = request.data.get('user_id')
    print("Received user_id:", user_id)

    if not user_id:
        return JsonResponse({'error': 'user_id parameter is required'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

    places = Places.objects.all()
    places_list = []

    for place in places:
        places_list.append({
            'id': place.id,
            'user_id': place.user.id,
            'name': place.name,
            'description': place.description,
            'location': place.location,
            'image_url_1': place.image_url_1,
            'image_url_2': place.image_url_2,
            'image_url_3': place.image_url_3,
            'created_at': place.created_at,
            'updated_at': place.updated_at
        })

    # If you just wanted to test a sample key
   

    return JsonResponse({'places': places_list}, status=200)

