from .models import Team
from rest_framework.views import APIView, Response, Request, status
from utils import data_processing, ImpossibleTitlesError, InvalidYearCupError, NegativeTitleError
from django.forms.models import model_to_dict

class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        teams_list = []

        for team in teams:
            teams_dict = model_to_dict(team)
            teams_list.append(teams_dict)

        return Response(teams_list, status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
        except (ImpossibleTitlesError, InvalidYearCupError, NegativeTitleError) as error:
            return Response(
                {"error": error.args[0]}, status.HTTP_400_BAD_REQUEST
            )

        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_201_CREATED)

    
class TeamDetailView(APIView):
     def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id = team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
    
        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)


     def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id = team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

     def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id = team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        team.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

