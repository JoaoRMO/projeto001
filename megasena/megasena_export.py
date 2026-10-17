#!/usr/bin/env python3
"""Baixa os resultados da Mega-Sena (API da Caixa) e gera um CSV com uma linha por concurso.

Uso:
    python3 megasena_export.py                      # concursos 1 a 3070 -> megasena.csv
    python3 megasena_export.py --inicio 2900 --fim 3070

Cada JSON baixado fica salvo em --cache (padrão: megasena_json/). Se o script for
interrompido, rodar de novo continua de onde parou, sem baixar tudo outra vez.
Usa apenas a biblioteca padrão do Python (não precisa instalar nada).
"""

import argparse
import csv
import json
import os
import re
import time
import urllib.request
from datetime import datetime

URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/{}"

# Faixas de premiação que aparecem no CSV (acertos -> colunas de ganhadores e prêmio).
FAIXAS = ("6", "5", "4")

COLUNAS = [
    "concurso",
    "data",
    "dezena_1", "dezena_2", "dezena_3", "dezena_4", "dezena_5", "dezena_6",
    "sorteio_ordem_1", "sorteio_ordem_2", "sorteio_ordem_3",
    "sorteio_ordem_4", "sorteio_ordem_5", "sorteio_ordem_6",
    "acumulado",
    "ganhadores_6", "premio_6",
    "ganhadores_5", "premio_5",
    "ganhadores_4", "premio_4",
    "valor_arrecadado",
    "valor_acumulado_concurso_0_5",
    "valor_acumulado_concurso_especial",
    "valor_acumulado_proximo_concurso",
    "valor_estimado_proximo_concurso",
    "data_proximo_concurso",
    "local_sorteio",
    "municipio_uf_sorteio",
]


def obter(concurso, cache_dir, pausa, tentativas=3):
    """Devolve o JSON do concurso, lendo do cache se já existir ou baixando da API."""
    arquivo = os.path.join(cache_dir, f"{concurso}.json")
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as f:
            return json.load(f)

    requisicao = urllib.request.Request(
        URL.format(concurso), headers={"User-Agent": "Mozilla/5.0"}
    )
    for tentativa in range(1, tentativas + 1):
        try:
            with urllib.request.urlopen(requisicao, timeout=30) as resposta:
                texto = resposta.read().decode("utf-8")
            break
        except OSError:
            if tentativa == tentativas:
                raise
            time.sleep(pausa * tentativa * 2)

    dados = json.loads(texto)
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(texto)
    time.sleep(pausa)  # pausa entre downloads para não sobrecarregar a API
    return dados


def data_iso(texto):
    """Converte 'dd/mm/aaaa' para 'aaaa-mm-dd'. Texto vazio vira string vazia."""
    if not texto:
        return ""
    return datetime.strptime(texto, "%d/%m/%Y").date().isoformat()


def linha(dados):
    """Transforma o JSON de um concurso em um dicionário com as colunas do CSV."""
    dezenas = sorted(dados["listaDezenas"])
    ordem = dados["dezenasSorteadasOrdemSorteio"]

    registro = {
        "concurso": dados["numero"],
        "data": data_iso(dados["dataApuracao"]),
        "acumulado": dados["acumulado"],
        "valor_arrecadado": dados["valorArrecadado"],
        "valor_acumulado_concurso_0_5": dados["valorAcumuladoConcurso_0_5"],
        "valor_acumulado_concurso_especial": dados["valorAcumuladoConcursoEspecial"],
        "valor_acumulado_proximo_concurso": dados["valorAcumuladoProximoConcurso"],
        "valor_estimado_proximo_concurso": dados["valorEstimadoProximoConcurso"],
        "data_proximo_concurso": data_iso(dados["dataProximoConcurso"]),
        "local_sorteio": dados["localSorteio"].strip(),
        "municipio_uf_sorteio": dados["nomeMunicipioUFSorteio"].strip(),
    }

    for i, dezena in enumerate(dezenas, start=1):
        registro[f"dezena_{i}"] = dezena
    for i, dezena in enumerate(ordem, start=1):
        registro[f"sorteio_ordem_{i}"] = dezena

    for faixa in dados["listaRateioPremio"]:
        acertos = re.match(r"\d+", faixa["descricaoFaixa"]).group()
        if acertos in FAIXAS:
            registro[f"ganhadores_{acertos}"] = faixa["numeroDeGanhadores"]
            registro[f"premio_{acertos}"] = faixa["valorPremio"]

    return registro


def main():
    parser = argparse.ArgumentParser(description="Exporta os resultados da Mega-Sena para CSV.")
    parser.add_argument("--inicio", type=int, default=1, help="primeiro concurso (padrão: 1)")
    parser.add_argument("--fim", type=int, default=3070, help="último concurso (padrão: 3070)")
    parser.add_argument("--saida", default="megasena.csv", help="arquivo CSV de saída")
    parser.add_argument("--cache", default="megasena_json", help="pasta para os JSON baixados")
    parser.add_argument("--pausa", type=float, default=0.5, help="segundos entre downloads")
    args = parser.parse_args()

    os.makedirs(args.cache, exist_ok=True)
    registros = []

    for concurso in range(args.inicio, args.fim + 1):
        dados = obter(concurso, args.cache, args.pausa)
        if dados["numero"] != concurso:
            print(f"Aviso: pedi o concurso {concurso} e a API devolveu {dados['numero']}")
        registros.append(linha(dados))
        if concurso % 100 == 0:
            print(f"Concurso {concurso} processado")

    with open(args.saida, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS, restval="", extrasaction="raise")
        escritor.writeheader()
        escritor.writerows(registros)

    print(f"{len(registros)} concursos gravados em {args.saida}")


if __name__ == "__main__":
    main()
