import json
import pandas as pd
import re
from rapidfuzz import process, fuzz

ESSENCIAIS = [
    "academia", "piscina", "portaria 24h", "quadra poliesportiva", "churrasqueira",
    "salao de festas", "salao de jogos", "varanda gourmet", "elevador",
    "permite animais", "area de lazer", "mobiliado"
]

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
        return None, None
    valor_match = re.search(r"R\$ ?([\d.,]+)", campo)
    valor = float(valor_match.group(1).replace('.', '').replace(',', '.')) if valor_match else None
    periodos_alvo = {
        "mensal": ["mensal", "mês", "mesal", "ao mês", "mensais", "por mês", "mes"],
        "anual": ["anual", "ano", "por ano", "anualmente", "ano."],
    }
    campo_lower = campo.lower()
    periodo = None
    for target, variations in periodos_alvo.items():
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
        preco, _ = parse_valor_periodo_fuzzy(item.get('preco'))
        iptu, iptu_periodo = parse_valor_periodo_fuzzy(item.get('iptu'))
        condominio, condominio_periodo = parse_valor_periodo_fuzzy(item.get('condominio'))
        
        dados_imovel.append({
            'codigo': item.get('codigo'),
            'imobiliaria': item.get('imobiliaria'),
            'url_detalhes': item.get('url_detalhes'),
            'url_img': item.get('url_img'),
            'preco': preco,
            'tipo': item.get('tipo'),
            'dormitorios': item.get('dormitorios'),
            'metragem': item.get('metragem'),
            'vagas': item.get('vagas'),
            'data_captura': item.get('data_captura'),
            'descricao': item.get('descricao'),
            'iptu': iptu,
            'iptu_periodo': iptu_periodo,
            'condominio': condominio,
            'condominio_periodo': condominio_periodo
        })
        
        # Endereço (mesma lógica anterior)
        rua, bairro, cidade, estado = None, None, None, None
        endereco = item.get('endereco') or ''
        partes = [p.strip() for p in endereco.split(',')]
        if len(partes) >= 3:
            rua, bairro, cidade_estado = partes[0], partes[1], partes[2]
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

        ess = mapear_para_essenciais(item.get('caracteristicas', []))
        ess['codigo_imovel'] = item.get('codigo')
        dados_caracteristicas.append(ess)

    # Retorna dataframes, ou pode já salvar
    return (
        pd.DataFrame(dados_imovel),
        pd.DataFrame(dados_endereco),
        pd.DataFrame(dados_caracteristicas)
    )

def salvar_csvs(df_imovel, df_endereco, df_caracteristicas, pasta='data'):
    df_imovel.to_csv(f'{pasta}/imoveis.csv', index=False)
    df_endereco.to_csv(f'{pasta}/enderecos.csv', index=False)
    df_caracteristicas.to_csv(f'{pasta}/caracteristicas.csv', index=False)