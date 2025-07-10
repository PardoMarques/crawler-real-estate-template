from ollama.ollama_request import ollama_query


def extrair_condominio_ollama(texto_descricao, modelo="llama3"):
    prompt = f"""
    No texto a seguir, identifique e retorne APENAS o nome do condomínio, se houver. Caso não exista nome, responda apenas "NÃO ENCONTRADO".

    Texto: '''{texto_descricao}'''
    """
    resultado = ollama_query(prompt, model=modelo)
    # Limpa resposta genérica, se modelo for "falador"
    if "NÃO ENCONTRADO" in resultado.upper():
        return None
    return resultado