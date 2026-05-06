"""
Cálculo de impostos no Lucro Presumido.
"""

from calculadora_fiscal.utils.aliquotas import get_aliquota_icms

# Percentuais de presunção de lucro por atividade
PRESUNCAO = {
    "comercio":   0.08,
    "industria":  0.08,
    "servicos":   0.32,
}

# Alíquotas PIS e COFINS (cumulativo no Lucro Presumido)
PIS_ALIQUOTA    = 0.0065
COFINS_ALIQUOTA = 0.03

# IRPJ e CSLL incidem sobre o lucro presumido
IRPJ_ALIQUOTA  = 0.15
CSLL_ALIQUOTA  = 0.09

# Adicional IRPJ: 10% sobre lucro presumido que exceder R$20.000/mês
ADICIONAL_IRPJ = 0.10
LIMITE_ADICIONAL_MENSAL = 20_000.0


class LucroPresumido:
    def __init__(self, operacao: str, valor: float, uf: str, atividade: str):
        self.operacao = operacao
        self.valor = valor
        self.uf = uf
        self.atividade = atividade

    def calcular(self) -> dict:
        impostos = {}

        # PIS e COFINS (cumulativo)
        if self.operacao != "exportacao":
            impostos["pis"]    = self.valor * PIS_ALIQUOTA
            impostos["cofins"] = self.valor * COFINS_ALIQUOTA

        # ICMS (venda de produto e importação)
        if self.operacao in ("venda_produto", "importacao"):
            aliquota_icms = get_aliquota_icms(self.uf)
            impostos["icms"] = self.valor * aliquota_icms

        # ISS (prestação de serviços) - alíquota municipal padrão 5%
        if self.operacao == "venda_servico":
            impostos["iss"] = self.valor * 0.05

        # II - Imposto de Importação (alíquota genérica 20%)
        if self.operacao == "importacao":
            impostos["ii"] = self.valor * 0.20

        # Exportação: PIS/COFINS/ICMS isentos; IRPJ/CSLL incidem
        # IRPJ e CSLL sobre o lucro presumido
        presuncao = PRESUNCAO.get(self.atividade, 0.08)
        lucro_presumido = self.valor * presuncao

        irpj = lucro_presumido * IRPJ_ALIQUOTA
        if lucro_presumido > LIMITE_ADICIONAL_MENSAL:
            irpj += (lucro_presumido - LIMITE_ADICIONAL_MENSAL) * ADICIONAL_IRPJ

        impostos["irpj"] = irpj
        impostos["csll"] = lucro_presumido * CSLL_ALIQUOTA

        return impostos
