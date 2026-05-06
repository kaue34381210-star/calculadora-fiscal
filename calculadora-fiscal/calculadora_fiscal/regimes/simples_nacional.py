"""
Cálculo de impostos no Simples Nacional.
O DAS unifica: IRPJ, CSLL, PIS, COFINS, CPP, ICMS/ISS.
Alíquotas baseadas nos Anexos da LC 123/2006 (faixa inicial).
"""

from calculadora_fiscal.utils.aliquotas import get_aliquota_icms


# Alíquotas efetivas aproximadas para a 1ª faixa (até R$ 180.000/ano)
ALIQUOTAS_SIMPLES = {
    "venda_produto": 0.04,      # Anexo I - Comércio
    "venda_servico": 0.06,      # Anexo III - Serviços
    "importacao":    0.04,      # Anexo I
    "exportacao":    0.00,      # Exportações são isentas
}


class SimplesNacional:
    def __init__(self, operacao: str, valor: float, uf: str, atividade: str):
        self.operacao = operacao
        self.valor = valor
        self.uf = uf
        self.atividade = atividade

    def calcular(self) -> dict:
        aliquota = ALIQUOTAS_SIMPLES.get(self.operacao, 0.04)
        das = self.valor * aliquota

        if self.operacao == "exportacao":
            return {"das_exportacao_isento": 0.0}

        return {"simples": das}
