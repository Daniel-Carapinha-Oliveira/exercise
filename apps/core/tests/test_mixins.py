import pytest

from django.db import connection, models

from apps.core.mixins import MetaDataMixin

pytestmark = pytest.mark.django_db


class TestMetaDataMixin:
    class NewModelForTesting(MetaDataMixin, models.Model):
        class Meta:
            app_label = 'core'

    @pytest.fixture(autouse=True)
    def create_test_model_table(self):
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.NewModelForTesting)

    @pytest.fixture()
    def create_database_object(self, user_factory):
        user = user_factory()
        obj = self.NewModelForTesting.objects.create(created_by=user)
        return obj

    def test_model_inherits_four_attributes(self):
        expected_fields = ['created_at', 'deleted_at', 'created_by', 'deleted_by']
        actual_fields = [field.name for field in self.NewModelForTesting._meta.get_fields()]

        for field_name in expected_fields:
            assert field_name in actual_fields

    def test_model_inherits_correct_field_types(self):
        expected_fields = {
            'created_at': models.DateTimeField,
            'deleted_at': models.DateTimeField,
            'created_by': models.ForeignKey,
            'deleted_by': models.ForeignKey,
        }

        for field_name, field_type in expected_fields.items():
            field = self.NewModelForTesting._meta.get_field(field_name)
            # Assert that the field is an instance of the expected type
            assert isinstance(field, field_type), f"Field '{field_name}' should be a {field_type.__name__}"

    def test_created_at_field_not_null(self, create_database_object):
        obj = create_database_object

        assert obj.created_at is not None

    def test_deleted_at_field_null(self, create_database_object):
        obj = create_database_object

        assert not obj.deleted_at

    def test_deleted_by_field_null(self, create_database_object):
        obj = create_database_object

        assert not obj.deleted_by
