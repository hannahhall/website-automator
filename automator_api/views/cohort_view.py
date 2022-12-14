import json
import base64
from time import sleep
import requests
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from automator_api.models import Cohort, Student
from automator_api.views.admin_or_read_only import IsAdminOrReadOnly
from automator_api.views.multi_serializer_viewset import MultiSerializerViewSet
from automator_api.serializers import (
    CohortListSerializer, CohortCreateSerializer, CohortDetailSerializer,
)


class CohortViewSet(MultiSerializerViewSet):
    """
    List, Retrieve, Update, Create, Delete Cohorts
    """
    queryset = Cohort.objects.all()
    serializers = {
        'default': CohortListSerializer,
        'create': CohortCreateSerializer,
        'retrieve': CohortDetailSerializer,
    }

    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Cohort.objects.all().order_by('-demo_day')
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def create(self, request):
        serializer = CohortCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cohort = serializer.save()
        cohort.techs.set(request.data.get('techs', []))

        github_access = request.data['github_access']
        try:

            self.create_repo_from_template(cohort, github_access)
            if request.data['is_deployed']:
                sleep(10)
                self.create_env_file(cohort, github_access)
                sleep(10)
                self.deploy_site(cohort, github_access)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except RequestException as ex:
            ex_json = ex.response.json()
            message = ex_json['message']
            if ex.response.status_code == status.HTTP_403_FORBIDDEN:
                message += ', Go to your Github Application settings to grant permissions to the organization.'
            error_response = {
                'id': cohort.id,
                'message': message,
            }
            return Response(error_response, status=ex.response.status_code)

    def update(self, request, pk):
        cohort = Cohort.objects.get(pk=pk)
        serializer = CohortCreateSerializer(cohort, data=request.data)
        serializer.is_valid(raise_exception=True)
        cohort = serializer.save()
        cohort.techs.set(request.data.get('techs', []))

        return Response(serializer.data)

    @action(methods=['DELETE'], detail=True, url_path=r'techs/(?P<tech_pk>[^/.]+)')
    def techs(self, request, pk, tech_pk):
        """Remove a single tech from the cohort
        """
        cohort = Cohort.objects.get(pk=pk)
        cohort.techs.remove(tech_pk)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['DELETE'], detail=True, url_path=r'students/(?P<student_id>[^/.]+)')
    def students(self, request, pk, student_id):
        """Remove a single student from the cohort
        """
        cohort = Cohort.objects.get(pk=pk)
        student = Student.objects.get(student_id=student_id, cohort=cohort)
        student.cohort = None
        student.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True, url_path='deploy-website')
    def deploy_website(self, request, pk):
        cohort = Cohort.objects.get(pk=pk)
        github_access = request.data['github_access']
        try:
            if not cohort.repo_created:
                self.create_repo_from_template(cohort, github_access)
                sleep(10)

            if not cohort.is_deployed:
                self.create_env_file(cohort, github_access)
                sleep(10)
                self.deploy_site(cohort, github_access)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RequestException as ex:
            ex_json = ex.response.json()
            message = ex_json['message']
            if ex.response.status_code == status.HTTP_403_FORBIDDEN:
                message += ', Go to your Github Application settings to grant permissions to the organization.'
            error_response = {
                'id': cohort.id,
                'message': message,
            }
            return Response(error_response, status=ex.response.status_code)

    def create_repo_from_template(self, cohort, github_access_token):
        """Creates a github repo within the cohort's organization

        Args:
            cohort_org (string): the cohort's github org
            github_access_token (string): The user's github access token

        Returns:
            boolean: was the request successful
        """
        template = "nashville-software-school/class-website-template"
        url = f"https://api.github.com/repos/{template}/generate"

        payload = json.dumps({
            "owner": cohort.github_organization,
            "name": cohort.github_repo,
            "description": "The class website",
            "include_all_branches": True,
            "private": False,
        })
        headers = {
            'Authorization': f'Bearer {github_access_token}',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.ok:
            cohort.repo_created = response.ok
            cohort.save()
        else:
            raise RequestException(response=response)
        return response.ok

    def create_env_file(self, cohort, github_access_token):
        file_name = '.env.production'
        file_content = f'REACT_APP_SITE_TITLE="Meet NSS {cohort.name}"\nREACT_APP_COHORT_ID={cohort.id}\nREACT_APP_API=https://nss-automator.herokuapp.com/api'
        byte_content = file_content.encode('ascii')
        payload = json.dumps({
            'message': 'adding production env',
            'content': base64.b64encode(byte_content).decode('ascii'),
            'branch': 'develop',
        })

        headers = {
            'Authorization': f'Bearer {github_access_token}',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        url = f'https://api.github.com/repos/{cohort.github_organization}/{cohort.github_repo}/contents/{file_name}'

        response = requests.put(url, headers=headers, data=payload)

        return response.ok

    def deploy_site(self, cohort, github_access_token):
        """Deploy the class website with github pages

        Args:
            cohort_org (string): the cohort's github organization
            repo_name (string): the repo name

        Returns:
            boolean: was the request successful
        """
        url = f"https://api.github.com/repos/{cohort.github_organization}/{cohort.github_repo}/deployments"

        payload = json.dumps({
            'ref': 'main',
            'required_contexts': [],
        })
        headers = {
            'Authorization': f'Bearer {github_access_token}',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.ok:
            cohort.is_deployed = response.ok
            cohort.save()
        else:
            raise RequestException(response=response)
        return response.ok
