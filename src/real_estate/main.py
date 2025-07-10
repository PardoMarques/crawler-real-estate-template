import os
from transform.processar_dados import processar_imoveis, salvar_csvs
from transform.processar_dados import extrair_condominio_ollama 

if __name__ == "__main__":
    # 1. Executa o crawler
    os.system("scrapy crawl EvidenceImoveis -o ../data/scraping/raw/EvidenceImoveis.json")

    # 2. Processa e transforma
    df_imovel, df_endereco, df_caracteristicas = processar_imoveis("../data/scraping/raw/EvidenceImoveis.json")
    

    # 3. Salva os CSVs finais (prontos para análise ou carga no banco)
    salvar_csvs(df_imovel, df_endereco, df_caracteristicas)
    print("Pipeline finalizado!")