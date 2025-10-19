from django.shortcuts import render
from django_filters.views import FilterView
from .filters import ExerciseFilter
from apps.exercises.models import BodyPart, Exercise, Muscle, MusclePart
from django.http import JsonResponse

def muscles(request):
    all_muscles = Muscle.objects.all()
    return render(
        request,
        "muscles.html",
        {'current_page': 'exercises', 'muscles': all_muscles}
    )

def body_parts(request):
    all_body_parts = BodyPart.objects.all()
    return render(
        request,
        "body_parts.html",
        {'current_page': 'exercises', 'body_parts': all_body_parts}
    )

class Exercises(FilterView):
    model = Exercise
    filterset_class = ExerciseFilter
    template_name = 'exercises.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Copy GET parameters and remove 'page' so it doesn't conflict with pagination
        querydict = self.request.GET.copy()
        querydict.pop('page', None)
        context['querystring'] = querydict.urlencode()
        context['current_page'] = 'exercises'
        return context

def get_muscles(request):
    body_part_id = request.GET.get('body_part')
    muscles = Muscle.objects.filter(body_part_id=body_part_id).values('id', 'name')
    return JsonResponse(list(muscles), safe=False)

def get_muscle_parts(request):
    muscle_id = request.GET.get('muscle')
    parts = MusclePart.objects.filter(muscle_id=muscle_id).values('id', 'name')
    return JsonResponse(list(parts), safe=False)

# TODO: add api to allow to add exercise, create a user and give to recruiter.