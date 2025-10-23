import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django_filters.views import FilterView
from django.http import JsonResponse
from django.urls import reverse
from io import BytesIO
from PIL import Image
from rest_framework.test import APIClient

from apps.exercises.filters import ExerciseFilter
from apps.exercises.models import (
    MuscleGroup,
    Muscle,
    MusclePart,
    Exercise
)
from apps.exercises.views import Exercises

pytestmark = pytest.mark.django_db


class TestMuscleGroupsPageView:
    def test_view_loads_successfully(self, client):
        response = client.get(reverse('muscle_groups_page'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse('muscle_groups_page'))
        assert 'muscle_groups.html' in [template.name for template in response.templates]

    def test_view_has_correct_context(self, client, muscle_group_factory):
        muscle_group_factory.create_batch(10)

        response = client.get(reverse('muscle_groups_page'))

        assert 'current_page' in response.context
        assert response.context['current_page'] == 'exercises'

        assert 'muscle_groups' in response.context
        assert list(response.context['muscle_groups']) == list(MuscleGroup.objects.all())


class TestGetMusclesQuerysetView:
    def test_view_loads_successfully(self, client):
        response = client.get(reverse('get_muscles_queryset'))
        assert response.status_code == 200

    def test_returns_muscles_for_given_group(self, client, muscle_group_factory, muscle_factory):
        muscle_group_1 = muscle_group_factory.create(name="muscle_group_1")
        muscle_group_2 = muscle_group_factory.create(name="muscle_group_2")

        muscle_1_for_muscle_group_1 = muscle_factory.create(name="muscle_1", muscle_group=muscle_group_1)
        muscle_2_for_muscle_group_1 = muscle_factory.create(name="muscle_2", muscle_group=muscle_group_1)

        muscle_factory.create(name="muscle_group_3", muscle_group=muscle_group_2)

        url = reverse('get_muscles_queryset')
        response = client.get(url, {'muscle_group': muscle_group_1.id})

        assert response.status_code == 200
        data = response.json()
        expected = list(Muscle.objects.filter(muscle_group=muscle_group_1).values('id', 'name'))

        assert data == expected
        assert all(muscle['id'] in [muscle_1_for_muscle_group_1.id, muscle_2_for_muscle_group_1.id] for muscle in data)
        assert all(
            muscle['name'] in [muscle_1_for_muscle_group_1.name, muscle_2_for_muscle_group_1.name] for muscle in data)

    def test_returns_empty_list_for_nonexistent_group(self, client):
        response = client.get(reverse('get_muscles_queryset'), {'muscle_group': 999999})
        assert response.status_code == 200
        assert response.json() == []

    def test_response_is_json(self, client, muscle_group_factory, muscle_factory):
        group = muscle_group_factory()
        muscle_factory(muscle_group=group)

        response = client.get(reverse('get_muscles_queryset'), {'muscle_group': group.id})

        assert isinstance(response, JsonResponse)
        assert response['Content-Type'] == 'application/json'


class TestGetMusclePartsQuerysetView:
    def test_view_loads_successfully(self, client):
        response = client.get(reverse('get_muscle_parts_queryset'))
        assert response.status_code == 200

    def test_returns_parts_for_given_muscle(self, client, muscle_factory, muscle_part_factory):
        muscle_1 = muscle_factory.create(name="muscle_1")
        muscle_2 = muscle_factory.create(name="muscle_2")

        part_1_for_muscle_1 = muscle_part_factory.create(name="part_1", muscle=muscle_1)
        part_2_for_muscle_1 = muscle_part_factory.create(name="part_2", muscle=muscle_1)

        muscle_part_factory.create(name="part_3", muscle=muscle_2)

        url = reverse('get_muscle_parts_queryset')
        response = client.get(url, {'muscle': muscle_1.id})

        assert response.status_code == 200
        data = response.json()
        expected = list(MusclePart.objects.filter(muscle=muscle_1).values('id', 'name'))

        assert data == expected
        assert all(part['id'] in [part_1_for_muscle_1.id, part_2_for_muscle_1.id] for part in data)
        assert all(part['name'] in [part_1_for_muscle_1.name, part_2_for_muscle_1.name] for part in data)

    def test_returns_empty_list_for_nonexistent_muscle(self, client):
        response = client.get(reverse('get_muscle_parts_queryset'), {'muscle': 999999})
        assert response.status_code == 200
        assert response.json() == []

    def test_response_is_json(self, client, muscle_factory, muscle_part_factory):
        muscle = muscle_factory()
        muscle_part_factory(muscle=muscle)

        response = client.get(reverse('get_muscle_parts_queryset'), {'muscle': muscle.id})

        assert isinstance(response, JsonResponse)
        assert response['Content-Type'] == 'application/json'


class TestExercisesView:
    def test_view_loads_successfully(self, client):
        url = reverse('exercises')
        response = client.get(url)
        assert response.status_code == 200

    def test_model_is_exercise(self):
        assert Exercises.model.__name__ == 'Exercise'

    def test_inherits_filter_view(self):
        assert issubclass(Exercises, FilterView)

    def test_filterset_class_is_exercise_filter(self):
        assert Exercises.filterset_class == ExerciseFilter

    def test_view_has_correct_context(self, client):
        response = client.get(reverse('exercises'), {'muscle_group': 1, 'page': 1})

        assert 'current_page' in response.context
        assert response.context['current_page'] == 'exercises'

        assert 'querystring' in response.context
        assert response.context['querystring'] == 'muscle_group=1'

    def test_get_queryset_returns_distinct(
            self,
            exercise_factory,
            muscle_factory,
            muscle_group_factory,
            muscle_part_factory,
            client
    ):
        muscle_group = muscle_group_factory()
        muscle = muscle_factory(muscle_group=muscle_group)

        muscle_part1 = muscle_part_factory(muscle=muscle)
        muscle_part2 = muscle_part_factory(muscle=muscle)

        exercise_factory(name='exercise_1', muscle_part=[muscle_part1, muscle_part2])
        exercise_factory(name='exercise_2', muscle_part=[muscle_part2])

        filter_data = {
            'muscle_group': muscle_group.id,
            'muscle': muscle.id,
            'muscle_part': muscle_part1.id
        }

        f = ExerciseFilter(filter_data, queryset=Exercise.objects.all())

        filtered_qs = f.qs

        # should return exactly 1 exercise, but returns more because of many-to-many relationship.
        assert len(filtered_qs) != len(filtered_qs.distinct())

        url = reverse('exercises') + f"?muscle_group={muscle_group.id}&muscle={muscle.id}&muscle_part={muscle_part1.id}"
        response = client.get(url)
        exercises_in_context = response.context['object_list']
        assert exercises_in_context.count() == 1


class TestExerciseAPIViewView:
    client = APIClient()

    @pytest.fixture(autouse=True)
    def authenticate_user(self, user_factory):
        user_password = 'testpass'
        user = user_factory()
        user.set_password(user_password)
        user.save()

        self.client.login(username=user.username, password=user_password)

    def test_get_returns_all_exercises(self, exercise_factory):
        exercise_factory.create_batch(10)

        response = self.client.get(reverse('api_exercises'))

        assert response.status_code == 200
        assert len(response.json()) == 10

    def test_post_saves_object(self, muscle_part_factory):
        muscle_part = muscle_part_factory()

        image = Image.new('RGB', (1, 1), color='white')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", buffer.read(), content_type="image/jpeg")

        payload = {
            "name": "Push Up",
            "description": "Upper body exercise",
            "workout_type": "calisthenics",
            "muscle_part": [muscle_part.name],
            "image": image_file
        }

        assert Exercise.objects.count() == 0

        response = self.client.post(reverse('api_exercises'), data=payload, format='multipart')

        assert response.status_code == 201
        assert Exercise.objects.count() == 1
