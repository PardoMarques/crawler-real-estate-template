from datetime import datetime
import os
from transform.processar_dados import processar_imoveis, salvar_csvs

date_str = datetime.now().strftime("%Y_%m_%d_%H_%M")
if __name__ == "__main__":
    # 1. Executa o crawler
    os.system(f"scrapy crawl EvidenceImoveis -o ../data/scraping/raw/{date_str}_EvidenceImoveis.json")

    # 2. Processa e transforma
    df_imovel, df_endereco, df_caracteristicas = processar_imoveis(f"../data/scraping/raw/{date_str}_EvidenceImoveis.json")

    # 3. Salva os CSVs finais (prontos para análise ou carga no banco)
    salvar_csvs(df_imovel, df_endereco, df_caracteristicas, date_str)
    print("Pipeline finalizado!")