"""
Formatação dos resultados no terminal.
"""

import json


NOMES_IMPOSTOS = {
    "simples": "Simples Nacional (DAS)",
    "irpj": "IRPJ",
    "csll": "CSLL",
    "pis": "PIS",
    "cofins": "COFINS",
    "icms": "ICMS",
    "iss": "ISS",
    "ipi": "IPI",
    "ii": "II (Imposto de Importação)",
    "iof": "IOF",
}

NOMES_OPERACOES = {
    "venda_produto": "Venda de Produto",
    "venda_servico": "Prestação de Serviço",
    "importacao": "Importação",
    "exportacao": "Exportação",
}

NOMES_REGIMES = {
    "simples": "Simples Nacional",
    "presumido": "Lucro Presumido",
    "real": "Lucro Real",
}


def formatar_reais(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_resultado(resultado: dict, como_json: bool = False):
    if como_json:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        return

    regime = NOMES_REGIMES.get(resultado["regime"], resultado["regime"])
    operacao = NOMES_OPERACOES.get(resultado["operacao"], resultado["operacao"])

    print("\n" + "=" * 55)
    print("        CALCULADORA FISCAL - RESULTADO")
    print("=" * 55)
    print(f"  Regime Tributário : {regime}")
    print(f"  Operação          : {operacao}")
    print(f"  UF                : {resultado['uf']}")
    print(f"  Valor da Operação : {formatar_reais(resultado['valor_operacao'])}")
    print("-" * 55)
    print("  IMPOSTOS INCIDENTES:")

    for imposto, valor in resultado["impostos"].items():
        nome = NOMES_IMPOSTOS.get(imposto, imposto.upper())
        pct = (valor / resultado["valor_operacao"]) * 100
        print(f"    {nome:<30} {formatar_reais(valor):>12}  ({pct:.2f}%)")

    print("-" * 55)
    print(f"  Total de Impostos : {formatar_reais(resultado['total_impostos'])}")
    print(f"  Carga Tributária  : {resultado['carga_tributaria_pct']:.2f}%")
    print(f"  Valor Líquido     : {formatar_reais(resultado['valor_liquido'])}")
    print("=" * 55 + "\n")
