from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer, GameSolutionSerializer


@api_view(["GET", 'POST', 'PUT'])
def game_view( request, game_id = None ):
    if request.method == 'POST':
        serializedGame = GameSerializer( data = {} )
        if serializedGame.is_valid():
            serializedGame.save()
            return Response( serializedGame.data )
        return Response( status=status.HTTP_400_BAD_REQUEST )
    
    try:
        game = Game.objects.get( pk = game_id )
    except Game.DoesNotExist:
        return Response( status = status.HTTP_404_NOT_FOUND )

    if request.method == 'PUT':
        serializedGame = GameSerializer( game, data=request.data )
        if serializedGame.is_valid():
            serializedGame.save()
            return Response( serializedGame.data )
        return Response( serializedGame.errors, status = status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        serializedGame = GameSerializer( game )
        return Response( serializedGame.data )

@api_view(['GET'])
def game_solution( request, game_id = None ):
    try:
        game = Game.objects.get( pk = game_id )
    except Game.DoesNotExist:
        return Response( status = status.HTTP_404_NOT_FOUND )

    if request.method == 'GET':
        return Response( GameSolutionSerializer( game, many = False ).data )
    else:
        # Framework should be handling this case
        pass
