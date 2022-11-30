import os
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def authenticate_github(request):
    # https://github.com/login/oauth/authorize?scope=user:email,repo_deployment,repo,admin_org&client_id=115cd11b75337ea75fdd
    session_code = request.query_params['code']

  # ... and POST it back to GitHub
    result = requests.post(
        'https://github.com/login/oauth/access_token',
        {
            'client_id': os.environ.get('GH_CLIENT_ID'),
            'client_secret': os.environ.get('GH_CLIENT_SECRET'),
            'code': session_code
        },
        headers={'Accept': 'application/json'}
    )
    json = result.json()
    # extract the token and granted scopes
    access_token = json['access_token']

    return Response({'github_token': access_token})

