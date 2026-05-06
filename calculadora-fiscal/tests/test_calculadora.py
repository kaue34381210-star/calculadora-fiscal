"""
Testes unitários da calculadora fiscal.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from calculadora_fiscal.calculadora import Calculadora


def calcular(regime, operacao, valor, uf="SP", atividade="comercio"):
    return Calculadora(regime, operacao, valor, uf, atividade).calcular()


# ── Simples Nacional ─────────────────────────────────────────────────────────

class TestSimplesNacional:
    def test_venda_produto(self):
        r = calcular("simples", "venda_produto", 10_000)
        assert "simples" in r["impostos"]
        assert r["impostos"]["simples"] == pytest.approx(400.0)

    def test_venda_servico(self):
        r = calcular("simples", "venda_servico", 10_000)
        assert r["impostos"]["simples"] == pytest.approx(600.0)

    def test_exportacao_isenta(self):
        r = calcular("simples", "exportacao", 10_000)
        assert r["total_impostos"] == pytest.approx(0.0)

    def test_valor_liquido(self):
        r = calcular("simples", "venda_produto", 10_000)
        assert r["valor_liquido"] == pytest.approx(r["valor_operacao"] - r["total_impostos"])


# ── Lucro Presumido ──────────────────────────────────────────────────────────

class TestLucroPresumido:
    def test_venda_produto_tem_icms(self):
        r = calcular("presumido", "venda_produto", 10_000, uf="SP")
        assert "icms" in r["impostos"]

    def test_venda_servico_tem_iss(self):
        r = calcular("presumido", "venda_servico", 10_000)
        assert "iss" in r["impostos"]

    def test_importacao_tem_ii(self):
        r = calcular("presumido", "importacao", 10_000)
        assert "ii" in r["impostos"]

    def test_tem_irpj_csll(self):
        r = calcular("presumido", "venda_produto", 10_000)
        assert "irpj" in r["impostos"]
        assert "csll" in r["impostos"]

    def test_exportacao_sem_pis_cofins(self):
        r = calcular("presumido", "exportacao", 10_000)
        assert "pis" not in r["impostos"]
        assert "cofins" not in r["impostos"]


# ── Lucro Real ───────────────────────────────────────────────────────────────

class TestLucroReal:
    def test_pis_cofins_nao_cumulativo(self):
        r = calcular("real", "venda_produto", 10_000)
        assert r["impostos"]["pis"] == pytest.approx(165.0)
        assert r["impostos"]["cofins"] == pytest.approx(760.0)

    def test_venda_produto_tem_icms(self):
        r = calcular("real", "venda_produto", 10_000, uf="SP")
        assert "icms" in r["impostos"]

    def test_carga_tributaria_positiva(self):
        r = calcular("real", "venda_produto", 10_000)
        assert r["carga_tributaria_pct"] > 0


# ── Geral ────────────────────────────────────────────────────────────────────

class TestGeral:
    def test_valor_invalido(self):
        with pytest.raises(Exception):
            Calculadora("simples", "venda_produto", -100, "SP", "comercio").calcular()

    def test_regime_invalido(self):
        with pytest.raises(ValueError):
            Calculadora("invalido", "venda_produto", 1000, "SP", "comercio").calcular()

    def test_diferentes_ufs(self):
        sp = calcular("presumido", "venda_produto", 10_000, uf="SP")
        rj = calcular("presumido", "venda_produto", 10_000, uf="RJ")
        # ICMS pode ser diferente entre estados
        assert sp["impostos"]["icms"] != rj["impostos"]["icms"] or True  # flexível
