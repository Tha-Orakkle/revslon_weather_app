from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

import os
import requests

from .serializer import UserSerializer, SearchSerializer
from .models import User, SearchHistory, SearchItem


class LandingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'message': 'Welcome',
            'enpoints': {
                'register': 'POST register/',
                'get token': 'POST token/',
                'refresh token ': 'POST token/refresh/',
                'weather (requires authentication)': 'GET weather/?city=cityName',
                'history/ (requires authentication)': 'GET history/'
            }
        })


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not username or not email or not password:
            return Response({'error': 'Please, provide complete credentials'}, status=400)
        try:
            User.objects.get(username=username.lower())
            return Response({'error': 'user with username already exists'}, status=400)
        except User.DoesNotExist:
            user = User(
                username=username.lower(),
                email=email.lower()
            )
            user.set_password(password)
            user.save()
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({
            'success': 'User created successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'data': serializer.data
        })


class GetWeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.GET.get('city', None)
        if not city:
            return Response({'error': 'Invalid city name'}, status=400)
        key = os.getenv('WEATHER_API_KEY')
        url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return Response({
                'error': data.message
            }, status=400)
        temp = data['current']['temp_c']

        SearchItem.objects.create(
            history=request.user.history,
            city=city
        )

        return Response({
            'success': f'The temparature in {city} is {temp} Celsius'
        })
    

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        history = user.history.searches.all()
        serializers = SearchSerializer(history, many=True)
        return Response({'data': serializers.data})

