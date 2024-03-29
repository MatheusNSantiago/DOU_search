from datetime import date
from src.infrastructure.teams.teams import Endpoints, enviar_sumula_para_o_teams


def lambda_handler(event, context):

    sumula = event["body"]
    if event["status"] == "VAZIO":
        sumula = {}

    enviar_sumula_para_o_teams(
        sumula,
        dia=date.today(),
        api_endpoint=Endpoints.OFICIAL,
    )

    return {
        "body": f"A súmula do dia {date.today()} foi encaminhada para o grupo do teams com sucesso",
        "status": "OK",
    }
