from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.ML.functions import predict_troop_conf


@api_view(['POST',])
def get_conf(request):
    if request.method == 'POST':
        info_towers = request.data
        predict_troops = predict_troop_conf(info_towers)
        return Response(predict_troops, status=status.HTTP_200_OK)