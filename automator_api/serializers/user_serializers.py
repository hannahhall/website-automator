from collections import OrderedDict
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

from automator_api.models import Student


class StudentDetailSerializer(serializers.ModelSerializer):
    """Student model serializer

    fields: student_id, bio, github_handle, linkedin, resume_link,
            podcast_link, cohort, favorite_quote, image
    """
    class Meta:
        model = Student
        fields = ('bio', 'github_handle', 'linkedin', 'resume_link',
                  'podcast_link', 'favorite_quote', 'circle_image',
                  'first_name', 'last_name', 'email', 'cohort_name',)

    def to_representation(self, instance):
        """Object instance -> Dict of primitive datatypes."""
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:

            attribute = field.get_attribute(instance)

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(
                attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                value = None
            else:
                value = field.to_representation(attribute)

            ret[field.field_name] = {
                'value': value,
                'verbose_name': field.label,
            }

        return ret


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')


class UpdateStudentSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = Student
        fields = ('bio', 'github_handle', 'linkedin', 'resume_link',
                  'podcast_link', 'cohort', 'favorite_quote', 'circle_image', 'user', 'image')
        extra_kwargs = {
            'image': {'write_only': True}
        }

    def update(self, instance, validated_data):
        user_serializer = self.fields['user']
        og_user = instance.user
        updated_user = validated_data.pop('user')
        user_serializer.update(og_user, updated_user)

        return super().update(instance, validated_data)


class CreateStudentSerializer(serializers.ModelSerializer):
    """Used in RegisterView

    fields: bio, github_handle, linkedin, resume_link,
            podcast_link, cohort, favorite_quote, image
    """
    class Meta:
        model = Student
        fields = ('bio', 'github_handle', 'linkedin', 'resume_link',
                  'podcast_link', 'cohort', 'favorite_quote', 'image')


class UserSerializer(serializers.ModelSerializer):
    """For UserView get and post responses

    fields: first_name, last_name, username, student, is_staff
    """

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'is_staff')


class StudentListSerializer(serializers.ModelSerializer):
    """For viewing a list of students

    fields:
        student_id, full_name, is_complete
    """
    class Meta:
        model = Student
        fields = ('student_id', 'full_name', 'is_complete')
