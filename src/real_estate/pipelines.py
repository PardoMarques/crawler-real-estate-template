from itemadapter import ItemAdapter
import re
from rapidfuzz import process, fuzz
from real_estate.transform.processar_dados import ESSENCIAIS, mapear_para_essenciais, parse_valor_periodo_fuzzy

class CleanRealStatePipeline:
    def process_item(self, item, spider):
        
        # 1. Aplica o fuzzy mapping nas características
        essenciais = mapear_para_essenciais(item.get('caracteristicas', ESSENCIAIS, []))
        for nome, valor in essenciais.items():
            item[nome] = valor
        
        # 2. Processa os valores de preço, iptu, condominio, etc.
        preco, _ = parse_valor_periodo_fuzzy(item.get('preco'))
        iptu, iptu_periodo = parse_valor_periodo_fuzzy(item.get('iptu'))
        condominio, condominio_periodo = parse_valor_periodo_fuzzy(item.get('condominio'))

        item['preco'] = preco
        item['iptu'] = iptu
        item['iptu_periodo'] = iptu_periodo
        item['condominio'] = condominio
        item['condominio_periodo'] = condominio_periodo
        
        return item

class OllamaRealStatePipeline:
    def process_item(self, item, spider):
        return item
