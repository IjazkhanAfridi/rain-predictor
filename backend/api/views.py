from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import PredictionRequest
from .serializers import (
    SignupSerializer, 
    LoginSerializer, 
    UserSerializer,
    PredictionInputSerializer,
    PredictionRequestSerializer
)
from .services import RainPredictionService


class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        'success': True,
                        'message': 'Login successful',
                        'data': {
                            'user': {
                                'id': user.id,
                                'email': user.email,
                                'username': user.username
                            },
                            'tokens': {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)
                            }
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'success': False,
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        
        if serializer.is_valid():
            location = serializer.validated_data['location']
            date = serializer.validated_data['date']
            
            prediction_result = RainPredictionService.predict_rain(location, date)
            
            if not prediction_result.get('success', False):
                return Response({
                    'success': False,
                    'error': prediction_result.get('error', 'Prediction failed')
                }, status=status.HTTP_400_BAD_REQUEST)
            
            prediction_request = PredictionRequest.objects.create(
                user=request.user,
                location=location,
                date=date,
                prediction_result=prediction_result['prediction'],
                confidence=prediction_result['confidence'],
                weather_data=prediction_result['weather_data']
            )
            
            return Response({
                'success': True,
                'message': 'Prediction completed successfully',
                'data': {
                    'id': prediction_request.id,
                    'location': location,
                    'date': str(date),
                    'prediction': prediction_result['prediction'],
                    'confidence': prediction_result['confidence'],
                    'weather_data': prediction_result['weather_data'],
                    'created_at': prediction_request.created_at
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        predictions = PredictionRequest.objects.filter(user=request.user)
        serializer = PredictionRequestSerializer(predictions, many=True)
        
        return Response({
            'success': True,
            'message': 'History retrieved successfully',
            'data': {
                'count': predictions.count(),
                'predictions': serializer.data
            }
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        
        return Response({
            'success': True,
            'data': {
                'user': serializer.data
            }
        }, status=status.HTTP_200_OK)
