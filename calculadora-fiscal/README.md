# 🧾 Calculadora Fiscal CLI

Ferramenta de linha de comando para cálculo de impostos em operações empresariais brasileiras, com suporte a todos os principais regimes tributários.

## 📋 Impostos calculados

| Imposto | Regimes |
|---|---|
| **DAS** (Simples Nacional) | Simples Nacional |
| **IRPJ** | Lucro Presumido, Lucro Real |
| **CSLL** | Lucro Presumido, Lucro Real |
| **PIS** | Lucro Presumido (cumulativo), Lucro Real (não-cumulativo) |
| **COFINS** | Lucro Presumido (cumulativo), Lucro Real (não-cumulativo) |
| **ICMS** | Lucro Presumido, Lucro Real (por UF) |
| **ISS** | Lucro Presumido, Lucro Real |
| **II** | Lucro Presumido, Lucro Real (importação) |

## 🚀 Instalação

```bash
git clone https://github.com/seu-usuario/calculadora-fiscal.git
cd calculadora-fiscal
pip install -r requirements.txt
```

## 💻 Uso

```bash
python main.py --regime <regime> --operacao <operacao> --valor <valor> [opções]
```

### Parâmetros

| Parâmetro | Opções | Obrigatório |
|---|---|---|
| `--regime` | `simples`, `presumido`, `real` | ✅ |
| `--operacao` | `venda_produto`, `venda_servico`, `importacao`, `exportacao` | ✅ |
| `--valor` | valor numérico em reais | ✅ |
| `--uf` | sigla do estado (ex: SP, RJ, MG) | ❌ (padrão: SP) |
| `--atividade` | `comercio`, `industria`, `servicos` | ❌ (padrão: comercio) |
| `--json` | saída em formato JSON | ❌ |

## 📌 Exemplos

### Venda de produto — Simples Nacional
```bash
python main.py --regime simples --operacao venda_produto --valor 50000
```

```
=======================================================
        CALCULADORA FISCAL - RESULTADO
=======================================================
  Regime Tributário : Simples Nacional
  Operação          : Venda de Produto
  UF                : SP
  Valor da Operação : R$ 50.000,00
-------------------------------------------------------
  IMPOSTOS INCIDENTES:
    Simples Nacional (DAS)         R$ 2.000,00  (4.00%)
-------------------------------------------------------
  Total de Impostos : R$ 2.000,00
  Carga Tributária  : 4.00%
  Valor Líquido     : R$ 48.000,00
=======================================================
```

### Prestação de serviço — Lucro Presumido
```bash
python main.py --regime presumido --operacao venda_servico --valor 30000 --atividade servicos
```

### Importação — Lucro Real (Minas Gerais)
```bash
python main.py --regime real --operacao importacao --valor 100000 --uf MG
```

### Saída em JSON
```bash
python main.py --regime presumido --operacao venda_produto --valor 20000 --json
```

## 🧪 Testes

```bash
pytest tests/ -v
```

## 🏗️ Estrutura do projeto

```
calculadora-fiscal/
├── main.py                          # Ponto de entrada CLI
├── calculadora_fiscal/
│   ├── calculadora.py               # Orquestrador principal
│   ├── regimes/
│   │   ├── simples_nacional.py      # Cálculos Simples Nacional
│   │   ├── lucro_presumido.py       # Cálculos Lucro Presumido
│   │   └── lucro_real.py            # Cálculos Lucro Real
│   └── utils/
│       ├── aliquotas.py             # Alíquotas ICMS por UF
│       └── formatador.py            # Formatação do output
└── tests/
    └── test_calculadora.py          # Testes unitários
```

## ⚠️ Aviso Legal

Este projeto é uma ferramenta educacional e de apoio. Os valores calculados são **estimativas baseadas em alíquotas gerais** e podem não refletir todas as particularidades de cada operação. Consulte sempre um contador ou advogado tributarista para decisões fiscais.

## 📄 Licença

MIT License — veja o arquivo [LICENSE](LICENSE) para detalhes.
