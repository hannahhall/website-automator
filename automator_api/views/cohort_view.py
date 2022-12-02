import json
from time import sleep
import requests
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.response import Response
from automator_api.models import Cohort
from automator_api.views.multi_serializer_viewset import MultiSerializerViewSet
from automator_api.serializers import CohortListSerializer, CohortCreateSerializer


class CohortViewSet(MultiSerializerViewSet):
    """
    List, Retrieve, Update, Create, Delete Cohorts
    """
    queryset = Cohort.objects.all()
    serializers = {
        'default': CohortListSerializer,
        'create': CohortCreateSerializer,
    }

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
                self.deploy_site(cohort, github_access)

            return Response(serializer.data)
        except RequestException as ex:
            ex_json = ex.response.json()
            message = ex_json['message']
            if ex.response.status_code == status.HTTP_403_FORBIDDEN:
                message += ' Go to your Github Application settings to grant permissions to the organization.'
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
        template = "nashville-software-school/Class-Website"
        url = f"https://api.github.com/repos/{template}/generate"

        payload = json.dumps({
            "owner": cohort.github_organization,
            "name": cohort.github_repo,
            "description": "The class website",
            "include_all_branches": False,
            "private": False
        })
        headers = {
            'Authorization': f'Bearer {github_access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.ok:
            cohort.repo_created = response.ok
            cohort.save()
        else:
            raise RequestException(response=response)
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
            "ref": 'master',
            'required_contexts': []
        })
        headers = {
            'Authorization': f'Bearer {github_access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.ok:
            cohort.is_deployed = response.ok
            cohort.save()
        else:
            raise RequestException(response=response)
        return response.ok
