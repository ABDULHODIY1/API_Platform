from modeltranslation.translator import translator, TranslationOptions
from .models import Post, Goal, Workout

class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

class GoalTranslationOptions(TranslationOptions):
    fields = ('name',)

class WorkoutTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Post, PostTranslationOptions)
translator.register(Goal, GoalTranslationOptions)
translator.register(Workout, WorkoutTranslationOptions)
