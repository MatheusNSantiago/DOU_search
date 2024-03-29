import os
import pandas as pd
from pandas.core.frame import DataFrame
from ..models.publicacao import Publicacao
from azure.cosmos import CosmosClient
import concurrent.futures
import requests
from ..utils import DateRange


def query_dou_remote(sql: str):
    client = CosmosClient(
        url=os.getenv("COSMOS_ACCOUNT_URI"),
        credential=os.getenv("COSMOS_ACCOUNT_KEY"),
    )

    db = client.get_database_client(os.getenv("COSMOS_DATABASE_ID"))
    container = db.get_container_client("dou")
    return list(container.query_items(sql, enable_cross_partition_query=True))


def pegar_dou_remote_db(date_range: DateRange):
    sql = f"SELECT * FROM c WHERE c.data BETWEEN '{date_range.inicio}' AND '{date_range.fim}'"

    pubs = [Publicacao.from_database(json) for json in query_dou_remote(sql)]

    return pd.DataFrame(pubs, columns=Publicacao.get_fields())