"""
Cálculo de impostos no Lucro Real.
PIS/COFINS não-cumulativos. IRPJ/CSLL sobre lucro real (estimado como % da receita).
"""

from calculadora_fiscal.utils.aliquotas import get_aliquota_icms

# PIS e COFINS (não-cumulativo)
PIS_ALIQUOTA    = 0.0165
COFINS_ALIQUOTA = 0.076

# IRPJ e CSLL — estimativa sobre margem de 10% (base ajustável)
MARGEM_LUCRO_ESTIMADA = 0.10
IRPJ_ALIQUOTA  = 0.15
CSLL_ALIQUOTA  = 0.09
ADICIONAL_IRPJ = 0.10
LIMITE_ADICIONAL_MENSAL = 20_000.0


class LucroReal:
    def __init__(self, operacao: str, valor: float, uf: str, atividade: str):
        self.operacao = operacao
        self.valor = valor
        self.uf = uf
        self.atividade = atividade

    def calcular(self) -> dict:
        impostos = {}

        # PIS e COFINS (não-cumulativo)
        if self.operacao != "exportacao":
            impostos["pis"]    = self.valor * PIS_ALIQUOTA
            impostos["cofins"] = self.valor * COFINS_ALIQUOTA

        # ICMS
        if self.operacao in ("venda_produto", "importacao"):
            aliquota_icms = get_aliquota_icms(self.uf)
            impostos["icms"] = self.valor * aliquota_icms

        # ISS
        if self.operacao == "venda_servico":
            impostos["iss"] = self.valor * 0.05

        # Imposto de Importação
        if self.operacao == "importacao":
            impostos["ii"] = self.valor * 0.20

        # IRPJ e CSLL sobre lucro estimado
        lucro_estimado = self.valor * MARGEM_LUCRO_ESTIMADA

        irpj = lucro_estimado * IRPJ_ALIQUOTA
        if lucro_estimado > LIMITE_ADICIONAL_MENSAL:
            irpj += (lucro_estimado - LIMITE_ADICIONAL_MENSAL) * ADICIONAL_IRPJ

        impostos["irpj"] = irpj
        impostos["csll"] = lucro_estimado * CSLL_ALIQUOTA

        return impostos
