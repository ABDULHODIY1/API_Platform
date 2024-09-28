from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import stripe

# Stripe API sozlamalari
stripe.api_key = settings.STRIPE_SECRET_KEY

class User(AbstractUser):
    """Foydalanuvchi modeli."""
    TYPE_CHOICES = [
        ("erkak", "Erkak"),
        ("ayol", "Ayol"),
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(blank=True, null=True)
    sex = models.CharField(max_length=6, blank=True, null=True, choices=TYPE_CHOICES)
    age = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email

class UserActivityLog(models.Model):
    """Foydalanuvchi faoliyati loglari."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity} ({self.timestamp})"

class PasswordResetRequest(models.Model):
    """Parolni tiklash so'rovi modeli."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.token}"

class UserProfile(models.Model):
    """Foydalanuvchi profili."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    """To'lovlar modeli."""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return self.user_profile.user.username

class Goal(models.Model):
    """Maqsad modeli."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Workout(models.Model):
    """Mashg'ulot modeli."""
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=50)
    duration = models.IntegerField()  # Mashg'ulot davomiyligi daqiqalarda
    video_url = models.URLField()

    def __str__(self):
        return self.name

class WorkoutLesson(models.Model):
    """Mashg'ulot darslari modeli."""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # Mashg'ulot dars davomiyligi daqiqalarda
    video_url = models.URLField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)  # Qo'shing
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class UserNotification(models.Model):
    """Foydalanuvchi xabarlari modeli."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"

class Insight(models.Model):
    """Foydalanuvchi haqida insightlar."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()
    workout_duration = models.IntegerField()
    calories_burned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class UserStatistic(models.Model):
    """Foydalanuvchi statistikasi."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField(default=0)
    calories_burned = models.FloatField(default=0)
    exercise_duration = models.IntegerField(default=0)  # Daqiqalarda

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Post(models.Model):
    """Ijtimoiy tarmoqdagi postlar modeli."""
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Food(models.Model):
    """Ovqatlanish uchun retseptlar modeli."""
    name = models.CharField(max_length=100)        # Retsept nomi
    preparation_time = models.IntegerField()       # Tayyorlanish vaqti (daqiqalarda)
    calories = models.FloatField()                 # Kaloriyalar miqdori
    water_intake = models.FloatField()             # Suv iste'moli (litrda)
    description = models.TextField()               # Retsept haqida qisqacha tavsif
    ingredients = models.TextField()               # Ingredientlar ro'yxati
    instructions = models.TextField()              # Tayyorlanish bosqichlari
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    """Mashg'ulotlar haqida ma'lumot modeli."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField(help_text="Calories burned")
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class MealPlan(models.Model):
    """Ovqatlanish rejalari modeli."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_calories = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class UserProgress(models.Model):
    """Foydalanuvchi rivoji modeli."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()
    calories_burned = models.IntegerField()
    workout_duration = models.IntegerField(help_text="Workout duration in minutes")

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class HealthTips(models.Model):
    """Salomatlik bo'yicha maslahatlar modeli."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=(
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise'),
        ('mental_health', 'Mental Health'),
    ))

    def __str__(self):
        return self.title

class ExternalAuth(models.Model):
    """Tashqi autentifikatsiya modeli."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    another_auth = models.CharField(max_length=100)
    another_auth_id = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class SomeModel(models.Model):
    """Yordamchi model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# models.py fayliga qo'shing
class UserGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.goal}"
