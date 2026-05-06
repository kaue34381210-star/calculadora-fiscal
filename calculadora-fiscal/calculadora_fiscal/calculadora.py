"""
Módulo principal que orquestra o cálculo de impostos.
"""

from calculadora_fiscal.regimes.simples_nacional import SimplesNacional
from calculadora_fiscal.regimes.lucro_presumido import LucroPresumido
from calculadora_fiscal.regimes.lucro_real import LucroReal


class Calculadora:
    REGIMES = {
        "simples": SimplesNacional,
        "presumido": LucroPresumido,
        "real": LucroReal,
    }

    def __init__(self, regime: str, operacao: str, valor: float, uf: str, atividade: str):
        self.regime = regime
        self.operacao = operacao
        self.valor = valor
        self.uf = uf
        self.atividade = atividade

    def calcular(self) -> dict:
        classe_regime = self.REGIMES.get(self.regime)
        if not classe_regime:
            raise ValueError(f"Regime tributário inválido: {self.regime}")

        engine = classe_regime(
            operacao=self.operacao,
            valor=self.valor,
            uf=self.uf,
            atividade=self.atividade,
        )

        impostos = engine.calcular()

        total_impostos = sum(v for v in impostos.values())

        return {
            "regime": self.regime,
            "operacao": self.operacao,
            "uf": self.uf,
            "valor_operacao": self.valor,
            "impostos": impostos,
            "total_impostos": total_impostos,
            "valor_liquido": self.valor - total_impostos,
            "carga_tributaria_pct": (total_impostos / self.valor) * 100,
        }
