from django.http import JsonResponse
from django.shortcuts import render
from django_filters.views import FilterView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.exercises.models import MuscleGroup, Exercise, Muscle, MusclePart

from .filters import ExerciseFilter
from .serializers import ExerciseSerializer


def muscle_groups_page(request):
    """
    Renders the muscle groups page view of the website using the "muscle_groups.html" template.

    Receives the HTTP request object.

    Returns an HttpResponse object containing the rendered muscle groups page.
    Passes a context dictionary containing:
        - current_page: identifies the active page as 'exercises'
        - muscle_groups: a queryset of all MuscleGroup objects retrieved from the database
    """
    all_muscle_groups = MuscleGroup.objects.all()
    return render(
        request,
        "muscle_groups.html",
        {'current_page': 'exercises', 'muscle_groups': all_muscle_groups}
    )


def get_muscles_queryset(request):
    """
    Returns a JSON response containing muscles filtered by a specified muscle group.

    Receives the HTTP request object with an optional 'muscle_group' parameter in the query string.

    Retrieves all Muscle objects whose muscle_group_id matches the provided parameter
    and converts them into a list of dictionaries containing:
        - id: the unique identifier of the muscle
        - name: the name of the muscle

    Returns a JsonResponse object with the list of muscles.
    """
    muscle_group_id = request.GET.get('muscle_group')
    muscles = Muscle.objects.filter(muscle_group_id=muscle_group_id).values('id', 'name')
    return JsonResponse(list(muscles), safe=False)


def get_muscle_parts_queryset(request):
    """
    Returns a JSON response containing muscle parts filtered by a specified muscle.

    Receives the HTTP request object with an optional 'muscle' parameter in the query string.

    Retrieves all MusclePart objects whose muscle_id matches the provided parameter
    and converts them into a list of dictionaries containing:
        - id: the unique identifier of the muscle part
        - name: the name of the muscle part

    Returns a JsonResponse object with the list of muscle parts.
    """
    muscle_id = request.GET.get('muscle')
    parts = MusclePart.objects.filter(muscle_id=muscle_id).values('id', 'name')
    return JsonResponse(list(parts), safe=False)


class Exercises(FilterView):
    """
    Displays a paginated, filterable list of Exercise objects using the "exercises.html" template.

    Inherits from Django's FilterView to provide filtering functionality through ExerciseFilter.

    Attributes:
        model: The Exercise model.
        filterset_class: The filter class used to filter Exercise objects.
        template_name: The template used to render the page.
        paginate_by: Number of exercises displayed per page.

    Methods:
        get_queryset(): Returns the filtered queryset of Exercise objects, ensuring
            distinct results and prefetching related muscle parts, muscles, and muscle groups.
        get_context_data(**kwargs): Adds additional context to the template, including:
            - querystring: The GET parameters (excluding 'page') encoded for pagination links
            - current_page: Identifies the active page as 'exercises'
    """
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
        """
        Part of API view for retrieving and creating Exercise objects.

        Attributes:\n
            - authentication_classes: Specifies Basic and Session authentication;
            - permission_classes: Requires the user to be authenticated;
            - http_method_names: Restricts allowed HTTP methods to 'get' and 'post'.

        get:\n
            Retrieves all Exercise objects from the database and returns them
            serialized as a list of ExerciseSerializer objects in the response.
        """
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Part of API view for retrieving and creating Exercise objects.

        Attributes:\n
            - authentication_classes: Specifies Basic and Session authentication;
            - permission_classes: Requires the user to be authenticated;
            - http_method_names: Restricts allowed HTTP methods to 'get' and 'post'.

        post:\n
            - Accepts new Exercise data in the request body, validates it using
            ExerciseSerializer, saves it with the currently authenticated user
            as 'created_by', and returns the serialized object with HTTP 201 status.
        """
        serializer = ExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # save object
        serializer.save(created_by=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
