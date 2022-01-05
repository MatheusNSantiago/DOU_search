from datetime import date
import pandas as pd
from pandas.core.frame import DataFrame

from .utils import tirar_acentuacao
from .filtro.filtro import Filtro
from .filtro.categorias.por_assinatura import FiltragemPorAssinatura
from .filtro.categorias.por_conteudo import FiltragemPorConteudo
from .filtro.categorias.por_ementa import FiltragemPorEmenta
from .filtro.categorias.por_escopo import FiltragemPorEscopo
from .filtro.categorias.por_motivo_geral import FiltragemPorMotivoGeral
from .filtro.categorias.por_titulo import FiltragemPorTitulo
from .infrastructure.repository import pegar_url_do_ingov


class DOU(Filtro):
    def __init__(self, df: DataFrame):
        self.df = df
        self.df.assinatura = self.df.assinatura.apply(tirar_acentuacao)

    def __call__(self) -> pd.DataFrame:
        pass 

    @property
    def filtrar_por_assinatura(self):
        return FiltragemPorAssinatura(self.df)

    @property
    def filtrar_por_conteudo(self):
        return FiltragemPorConteudo(self.df)

    @property
    def filtrar_por_ementa(self):
        return FiltragemPorEmenta(self.df)

    @property
    def filtrar_por_escopo(self):
        return FiltragemPorEscopo(self.df)

    @property
    def filtrar_por_motivo_geral(self):
        return FiltragemPorMotivoGeral(self.df)

    @property
    def filtrar_por_titulo(self):
        return FiltragemPorTitulo(self.df)

    def gerar_sumula(self, com_link_ingov=False) -> pd.DataFrame:
        resultado = pd.concat(
            [
                # # self.filtrar_por_motivo_geral(),
                self.filtrar_por_titulo(),
                self.filtrar_por_escopo(),
                self.filtrar_por_ementa(),
                self.filtrar_por_conteudo(),
                self.filtrar_por_assinatura(),
            ]
        )

        # | Adiciona motivo se a publicação foi achada por mais de uma categoria de filtragem
        duplicados = resultado[resultado.duplicated("id", keep=False)]
        sumula = resultado.drop_duplicates(subset="id")

        for i in duplicados.groupby("id").groups.values():
            index = i[0]

            motivos = duplicados.loc[index].motivo.to_list()
            motivos = "\n".join(motivos)

            sumula.loc[index].motivo = motivos

        # | Adiciona o link para o in.gov
        if com_link_ingov:
            sumula["pdf"] = sumula.id_materia.apply(lambda x: pegar_url_do_ingov(x))

        return sumula
