from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from cars.models import Car
from cars.serializers import CarSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def car_list(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            cars = cars.filter(title__icontains=title)
        
        cars_serializer = CarSerializer(cars, many=True)
        return JsonResponse(cars_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        car_data = JSONParser().parse(request)
        car_serializer = CarSerializer(data=car_data)
        if car_serializer.is_valid():
            car_serializer.save()
            return JsonResponse(car_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Car.objects.all().delete()
        return JsonResponse({'message': '{} cars were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def car_detail(request, pk):
    try: 
        car = Car.objects.get(pk=pk) 
    except Car.DoesNotExist: 
        return JsonResponse({'message': 'The car does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        car_serializer = CarSerializer(car) 
        return JsonResponse(car_serializer.data) 
 
    elif request.method == 'PUT': 
        car_data = JSONParser().parse(request) 
        car_serializer = CarSerializer(car, data=car_data) 
        if car_serializer.is_valid(): 
            car_serializer.save() 
            return JsonResponse(car_serializer.data) 
        return JsonResponse(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        car.delete() 
        return JsonResponse({'message': 'Car was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def car_list_published(request):
    cars = Car.objects.filter(published=True)
        
    if request.method == 'GET': 
        cars_serializer = CarSerializer(cars, many=True)
        return JsonResponse(cars_serializer.data, safe=False)
    