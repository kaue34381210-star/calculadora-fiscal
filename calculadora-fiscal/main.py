#!/usr/bin/env python3
"""
Calculadora Fiscal CLI
Ferramenta para cálculo de impostos em operações empresariais.
"""

import argparse
import sys
from calculadora_fiscal.calculadora import Calculadora
from calculadora_fiscal.utils.formatador import formatar_resultado


def main():
    parser = argparse.ArgumentParser(
        prog="calculadora-fiscal",
        description="Calculadora de impostos para operações empresariais",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--regime",
        choices=["simples", "presumido", "real"],
        required=True,
        help=(
            "Regime tributário da empresa:\n"
            "  simples   → Simples Nacional\n"
            "  presumido → Lucro Presumido\n"
            "  real      → Lucro Real"
        ),
    )

    parser.add_argument(
        "--operacao",
        choices=["venda_produto", "venda_servico", "importacao", "exportacao"],
        required=True,
        help=(
            "Tipo de operação:\n"
            "  venda_produto → Venda de mercadorias\n"
            "  venda_servico → Prestação de serviços\n"
            "  importacao    → Importação de produtos\n"
            "  exportacao    → Exportação de produtos"
        ),
    )

    parser.add_argument(
        "--valor",
        type=float,
        required=True,
        help="Valor da operação em reais (ex: 10000.00)",
    )

    parser.add_argument(
        "--uf",
        type=str,
        default="SP",
        help="UF para cálculo do ICMS (padrão: SP)",
    )

    parser.add_argument(
        "--atividade",
        type=str,
        default="comercio",
        choices=["comercio", "industria", "servicos"],
        help="Atividade da empresa para Lucro Presumido (padrão: comercio)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Exibe o resultado em formato JSON",
    )

    args = parser.parse_args()

    if args.valor <= 0:
        print("Erro: o valor da operação deve ser maior que zero.", file=sys.stderr)
        sys.exit(1)

    calc = Calculadora(
        regime=args.regime,
        operacao=args.operacao,
        valor=args.valor,
        uf=args.uf.upper(),
        atividade=args.atividade,
    )

    resultado = calc.calcular()
    formatar_resultado(resultado, args.json)


if __name__ == "__main__":
    main()
