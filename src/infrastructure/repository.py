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


# def inserir_publicacoes_dou_db(df: DataFrame):
#     """Coloca as publicações na database [dou] no (cosmosDB)"""

#     client = CosmosClient(
#         url=config.cosmos["ACCOUNT_URI"],
#         credential=config.cosmos["ACCOUNT_KEY"],
#     )
#     db = client.get_database_client(config.cosmos["DATABASE_ID"])
#     container = db.get_container_client("dou")

#     def _upsert(pub):
#         pub.update({"data": str(pub["data"])})

#         try:
#             container.upsert_item(pub)
#         except:
#             pub.update({"conteudo": pub["conteudo"][0:2500]})
#             container.upsert_item(pub)

#     total = 0
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         for _ in executor.map(_upsert, [i.to_dict() for i in df.iloc]):
#             total += 1
#             print(f"({total}/{len(df)}) = {round((total/len(df))*100, 2)}%")