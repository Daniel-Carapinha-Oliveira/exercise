from django.shortcuts import render
from django_filters.views import FilterView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import ExerciseSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status

from .filters import ExerciseFilter
from apps.exercises.models import MuscleGroup, Exercise, Muscle, MusclePart
from django.http import JsonResponse


def muscle_groups(request):
    all_muscle_groups = MuscleGroup.objects.all()
    return render(
        request,
        "muscle_groups.html",
        {'current_page': 'exercises', 'muscle_groups': all_muscle_groups}
    )


class Exercises(FilterView):
    model = Exercise
    filterset_class = ExerciseFilter
    template_name = 'exercises.html'
    paginate_by = 2

    def get_queryset(self):
        # Start with the filtered queryset from ExerciseFilter
        qs = super().get_queryset()
        # Ensure distinct to avoid duplicates caused by ManyToMany joins
        return qs.distinct().prefetch_related('muscle_part__muscle__muscle_group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Copy GET parameters and remove 'page' so it doesn't conflict with pagination
        querydict = self.request.GET.copy()
        querydict.pop('page', None)
        context['querystring'] = querydict.urlencode()
        context['current_page'] = 'exercises'
        return context


def get_muscles(request):
    muscle_group_id = request.GET.get('muscle_group')
    muscles = Muscle.objects.filter(muscle_group_id=muscle_group_id).values('id', 'name')
    return JsonResponse(list(muscles), safe=False)


def get_muscle_parts(request):
    muscle_id = request.GET.get('muscle')
    parts = MusclePart.objects.filter(muscle_id=muscle_id).values('id', 'name')
    return JsonResponse(list(parts), safe=False)


@extend_schema(
    tags=['Exercises'],
    request=ExerciseSerializer,
    responses=ExerciseSerializer(many=True)
)
class ExerciseAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get(self, request):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # save object
        serializer.save(created_by=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
