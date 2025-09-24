from django.shortcuts import render
from django_filters.views import FilterView
from .filters import ExerciseFilter
from apps.exercises.models import BodyPart, Exercise

def body_parts(request):
    all_body_parts = BodyPart.objects.all()
    return render(
        request,
        "body_parts.html",
        {'current_page': 'exercises', 'body_parts': all_body_parts}
    )

def exercises(request, body_part_id):
    exercises_queryset = Exercise.objects.filter(muscle_part__muscle__body_part_id=body_part_id)

    return render(request, "exercises.html", {
        'current_page': 'exercises',
        'exercises_queryset': exercises_queryset
    })

class AllExercises(FilterView):
    model = Exercise
    filterset_class = ExerciseFilter
    template_name = 'exercise_list.html'
    paginate_by = 2

    def get_queryset(self):
        # Optimize queries if you have related objects
        return super().get_queryset()

# TODO: add api to allow to add exercise, create a user and give to recruiter.