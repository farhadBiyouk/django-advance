from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view()
def api_get_list_view(request):
    return Response({'result': 'ok'})