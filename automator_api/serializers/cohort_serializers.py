from rest_framework import serializers
from automator_api.models import Cohort, Program, Student
from automator_api.serializers.tech_serializers import TechSerializer
from automator_api.serializers.user_serializers import UpdateStudentSerializer


class ProgramSerializer(serializers.ModelSerializer):
    """Program Model Serializer
    """
    class Meta:
        model = Program
        fields = ('name', 'id')


class CohortListSerializer(serializers.ModelSerializer):
    """Cohort Model Serializer for list view

    Fields:
        id, name
    """
    class Meta:
        model = Cohort
        fields = ('id', 'name', 'demo_day_readable', 'is_deployed')


class CohortCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('id', 'name', 'demo_day', 'demo_day_time', 'github_organization',
                  'slack_channel', 'program', 'techs', 'demo_day_link')


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('bio', 'github_handle', 'linkedin', 'resume_link',
                  'podcast_link', 'favorite_quote', 'circle_image',
                  'first_name', 'last_name', 'email', 'full_name', 'cohort_name', 'projects', 'student_id', 'is_complete')
        depth = 1


class CohortDetailSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    techs = TechSerializer(many=True)
    program = ProgramSerializer()

    def get_students(self, instance):
        students = instance.students.all().order_by('user__last_name')
        return StudentDetailSerializer(students, many=True).data

    class Meta:
        model = Cohort
        fields = ('id', 'name', 'demo_day_readable', 'demo_day_time', 'github_organization',
                  'slack_channel', 'program', 'techs', 'students', 'demo_day', 'is_deployed',
                  'student_count', 'demo_day_link', 'github_repo_link', 'deployed_link')

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
