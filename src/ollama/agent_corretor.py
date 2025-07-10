from ollama.ollama_request import ollama_query


def agente_imobiliario(texto, tipo_acao, contexto=None):
    print(0)
    
    # if tipo_acao == "extrair_condominio":
    #     # Usa seu prompt especializado
    #     return extrair_condominio_ollama(texto)
    # elif tipo_acao == "extrair_caracteristicas":
    #     return extrair_caracteristicas_ollama(texto)
    # elif tipo_acao == "buscar_valor_m2":
    #     bairro = extrair_bairro_ollama(texto)
    #     return buscar_valor_m2_bairro(bairro)
    # else:
    #     # Prompt genérico
    #     return ollama_query(f"Responda de acordo com o contexto: {contexto}\n{texto}")