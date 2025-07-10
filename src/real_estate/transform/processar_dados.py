import json
import pandas as pd
import re
from rapidfuzz import process, fuzz
import requests

ESSENCIAIS = [
    "academia", "piscina", "portaria 24h", "quadra poliesportiva", "churrasqueira",
    "salao de festas", "salao de jogos", "varanda gourmet", "elevador",
    "permite animais", "area de lazer", "mobiliado"
]

PERIODOS_ALVO = {
        "mensal": ["mensal", "mês", "mesal", "ao mês", "mensais", "por mês", "mes"],
        "anual": ["anual", "ano", "por ano", "anualmente", "ano."],
    }

def mapear_para_essenciais(caracs, essenciais=ESSENCIAIS, threshold=80):
    resultado = {essencial: False for essencial in essenciais}
    for c in caracs:
        c_l = c.strip().lower()
        match, score, _ = process.extractOne(c_l, essenciais, scorer=fuzz.token_sort_ratio)
        if score >= threshold:
            resultado[match] = True
    return resultado

def parse_valor_periodo_fuzzy(campo):
    if not campo:
        return None, "indefinido"
    valor_match = re.search(r"R\$ ?([\d.,]+)", campo)
    valor = float(valor_match.group(1).replace('.', '').replace(',', '.')) if valor_match else None
    
    campo_lower = campo.lower()
    periodo = "indefinido"  # valor padrão
    for target, variations in PERIODOS_ALVO.items():
        match, score, _ = process.extractOne(campo_lower, variations, scorer=fuzz.partial_ratio)
        if score >= 80:
            periodo = target
            break
    return valor, periodo

def processar_imoveis(json_path):
    with open(json_path, encoding='utf-8') as f:
        imoveis = json.load(f)

    dados_imovel = []
    dados_endereco = []
    dados_caracteristicas = []

    for item in imoveis:
        dados_imovel.append({
            'codigo': item.get('codigo'),
            'imobiliaria': item.get('imobiliaria'),
            'url_detalhes': item.get('url_detalhes'),
            'url_img': item.get('url_img'),
            'preco': item.get('preco'),
            'tipo': item.get('tipo'),
            'dormitorios': item.get('dormitorios'),
            'metragem': item.get('metragem'),
            'vagas': item.get('vagas'),
            'data_captura': item.get('data_captura'),
            'descricao': item.get('descricao'),
            'iptu': item.get('iptu'),
            'iptu_periodo': item.get('iptu_periodo'),
            'condominio': item.get('condominio'),
            'condominio_periodo': item.get('condominio_periodo')
        })

        rua, bairro, cidade, estado = None, None, None, None
        endereco = item.get('endereco') or ''
        partes = [p.strip() for p in endereco.split(',')]
        if len(partes) >= 3:
            rua = partes[0]
            bairro = partes[1]
            cidade_estado = partes[2]
            if '/' in cidade_estado:
                cidade, estado = cidade_estado.split('/')
            else:
                cidade = cidade_estado
        dados_endereco.append({
            'codigo_imovel': item.get('codigo'),
            'rua': rua,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado
        })

        ess = {}
        for essencial in ESSENCIAIS:
            ess[essencial] = item.get(essencial, False)
        ess['codigo_imovel'] = item.get('codigo')
        dados_caracteristicas.append(ess)

    return (
        pd.DataFrame(dados_imovel),
        pd.DataFrame(dados_endereco),
        pd.DataFrame(dados_caracteristicas)
    )

def salvar_csvs(df_imovel, df_endereco, df_caracteristicas, pasta='data'):
    df_imovel.to_csv(f'{pasta}/imoveis.csv', index=False)
    df_endereco.to_csv(f'{pasta}/enderecos.csv', index=False)
    df_caracteristicas.to_csv(f'{pasta}/caracteristicas.csv', index=False)

def extrair_condominio_ollama(texto_descricao):
    prompt = f"""
    No texto a seguir, identifique e retorne APENAS o nome do condomínio, se houver. Caso não exista nome, responda apenas "NÃO ENCONTRADO".

    Texto: '''{texto_descricao}'''
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    result = response.json()["response"].strip()
    # Limpa resposta genérica, se modelo for "falador"
    if "NÃO ENCONTRADO" in result.upper():
        return None
    return result

def aplicar_extracao_condominio(row):
    desc = row["descricao"]
    return extrair_condominio_ollama(desc)