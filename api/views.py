from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action  
from django.contrib.auth import login, logout
from django.conf import settings
import stripe
from .models import Food 
from .models import (
    User, UserProfile, ExternalAuth, Goal, UserGoal,
    Workout, WorkoutLesson, Notification, Insight,
    UserNotification, Post, Food, Exercise, MealPlan,
    UserProgress, HealthTips, PasswordResetRequest,
    UserActivityLog, Payment
)
import uuid
from rest_framework import generics
from .serializers import (
    UserSerializer, UserProfileSerializer, ExternalAuthSerializer,
    GoalSerializer, UserGoalSerializer, WorkoutSerializer,
    WorkoutLessonSerializer, NotificationSerializer, InsightSerializer,
    UserNotificationSerializer, PostSerializer, FoodSerializer,
    ExerciseSerializer, MealPlanSerializer, UserProgressSerializer,
    HealthTipsSerializer, UserRegistrationSerializer,
    UserLoginSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetSerializer,
    UserActivityLogSerializer, PaymentSerializer
)
from rest_framework import viewsets
from .models import UserActivityLog, PasswordResetRequest
from .serializers import UserActivityLogSerializer, PasswordResetRequestSerializer
from rest_framework import viewsets
from .models import Food
from .serializers import FoodSerializer
from rest_framework import viewsets
from .models import SomeModel
from .serializers import SomeModelSerializer
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, UserProfile
from .serializers import PaymentSerializer
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# class PaymentCreateViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

#     def create(self, request):
#         user_profile = UserProfile.objects.get(user=request.user)
#         amount = request.data.get('amount')
        
#         try:
#             amount_in_cents = int(float(amount) * 100)
#         except ValueError:
#             return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             charge = stripe.Charge.create(
#                 amount=amount_in_cents,
#                 currency='usd',
#                 customer=user_profile.stripe_customer_id,
#                 description=f'Charge for {user_profile.user.email}'
#             )

#             payment = Payment.objects.create(
#                 user_profile=user_profile,
#                 stripe_charge_id=charge.id,
#                 amount=amount,
#                 success=True
#             )
#             return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
#         except stripe.error.StripeError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer

class PasswordResetRequestViewSet(viewsets.ModelViewSet):
    queryset = PasswordResetRequest.objects.all()
    serializer_class = PasswordResetRequestSerializer


class SomeModelViewSet(viewsets.ModelViewSet):
    queryset = SomeModel.objects.all()
    serializer_class = SomeModelSerializer

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Bunda `User` modeli bo'lishi kerak
    serializer_class = UserSerializer  # Bunda to'g'ri serializer aniqlangan bo'lishi kerak

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @action(detail=False, methods=['get'])
    def high_protein(self, request):
        high_protein_foods = self.queryset.filter(protein__gte=20)
        serializer = self.get_serializer(high_protein_foods, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_carb(self, request):
        low_carb_foods = self.queryset.filter(carbs__lte=10)
        serializer = self.get_serializer(low_carb_foods, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def vegetarian(self, request):
        vegetarian_foods = self.queryset.filter(is_vegetarian=True)
        serializer = self.get_serializer(vegetarian_foods, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def total_calories(self, request):
        food_ids = request.data.get('food_ids', [])
        selected_foods = self.queryset.filter(id__in=food_ids)
        total_calories = sum(food.calories for food in selected_foods)
        return Response({'total_calories': total_calories})

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_calories = self.request.query_params.get('min_calories')
        if min_calories:
            queryset = queryset.filter(calories_burned__gte=min_calories)
        return queryset

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(user=user, date__range=[date_from, date_to])
        return queryset

class HealthTipsViewSet(viewsets.ModelViewSet):
    queryset = HealthTips.objects.all()
    serializer_class = HealthTipsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ExternalAuthViewSet(viewsets.ModelViewSet):
    queryset = ExternalAuth.objects.all()
    serializer_class = ExternalAuthSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class UserGoalViewSet(viewsets.ModelViewSet):
    queryset = UserGoal.objects.all()
    serializer_class = UserGoalSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutLessonViewSet(viewsets.ModelViewSet):
    queryset = WorkoutLesson.objects.all()
    serializer_class = WorkoutLessonSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class InsightViewSet(viewsets.ModelViewSet):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer

class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer

class PaymentCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        amount = request.data.get('amount')
        try:
            amount_in_cents = int(float(amount) * 100)
        except ValueError:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency='usd',
                customer=user_profile.stripe_customer_id,
                description=f'Charge for {user_profile.user.email}'
            )

            payment = Payment.objects.create(
                user_profile=user_profile,
                stripe_charge_id=charge.id,
                amount=amount,
                success=True
            )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.data.get("email")).first()
            if user:
                token = str(uuid.uuid4())
                PasswordResetRequest.objects.create(user=user, token=token)
                return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            reset_request = PasswordResetRequest.objects.filter(token=serializer.data.get("token"), is_used=False).first()
            if reset_request:
                user = reset_request.user
                user.set_password(serializer.data.get("new_password"))
                user.save()
                reset_request.is_used = True
                reset_request.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or used token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserActivityLog.objects.filter(user=self.request.user)
