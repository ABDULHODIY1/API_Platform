from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User, UserGoal, UserProfile, UserNotification, UserStatistic,
                     ExternalAuth, Workout, WorkoutLesson, Notification,
                     Insight, Goal, Payment, Post, Food, UserActivityLog,
                     PasswordResetRequest, Exercise, MealPlan, UserProgress,
                     HealthTips, SomeModel)

# Modellarni bir marta ro'yxatdan o'tkazing
admin.site.register(UserProfile)
admin.site.register(ExternalAuth)
admin.site.register(UserGoal)
admin.site.register(Workout)
admin.site.register(WorkoutLesson)
admin.site.register(Notification)
admin.site.register(Insight)
admin.site.register(UserNotification)
admin.site.register(Goal)
admin.site.register(Payment)
admin.site.register(UserStatistic)
admin.site.register(Food)
admin.site.register(UserActivityLog)
admin.site.register(PasswordResetRequest)
admin.site.register(Exercise)
admin.site.register(MealPlan)
admin.site.register(UserProgress)
admin.site.register(HealthTips)
admin.site.register(SomeModel)
admin.site.register(Post)

# User modelini UserAdmin bilan ro'yxatdan o'tkazing
admin.site.register(User, UserAdmin)
