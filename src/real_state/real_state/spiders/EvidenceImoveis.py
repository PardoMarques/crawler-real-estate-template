import scrapy

class EvidenceimoveisSpider(scrapy.Spider):
    name = "EvidenceImoveis"
    allowed_domains = ["www.evidenceimoveis.com.br"]
    start_urls = ["https://www.evidenceimoveis.com.br/busca/comprar/cidade/sao-paulo/bairros/agua-rasa_alto-da-mooca_analia-franco_belem_belenzinho_cangaiba_carrao_chacara-belenzinho_chacara-california_chacara-mafalda_cidade-mae-do-ceu_itaquera_jardim-analia-franco_jardim-textil_maranhao_mooca_mooca-baixa_parque-da-vila-prudente_parque-sao-jorge_penha_penha-de-franca_quinta-da-paineira_sacoma_tatuape_vila-alpina_vila-antonina_vila-brasilina_vila-carrao_vila-centenario_vila-diva-zona-leste_vila-ema_vila-formosa_vila-gomes-cardim_vila-invernada_vila-matilde_vila-nova-manchester_vila-prudente_vila-regente-feijo_vila-santa-clara_vila-santa-isabel_vila-zelina_vila-zilda/categoria/apartamento/valor_de/250000/valor_ate/10000000000/dormitorios/2/vagas/1/suites/1/area/40/1/"]
    
    # exemplo: ["https://www.evidenceimoveis.com.br/busca/comprar/cidade/sao-paulo/bairros/analia-franco/categoria/apartamento/valor_de/250000/valor_ate/1500000/dormitorios/2/vagas/1/suites/1/area/70/1/"] 

    def parse(self, response):
        blocos_imoveis = response.css("#resultados div.box-imovel")
        for bloco in blocos_imoveis:
            url_detalhes = bloco.css("a.link::attr(href)").get()
            url_img = bloco.css("img.lazy-cover::attr(src)").get()
            preco = bloco.css("span.valor::text").get()
            h2 = bloco.css("h2")
            bairro = h2.css("::text").get().strip().replace(',', '')
            cidade = h2.css("span::text").get()
            tipo = h2.css("small::text").get()
            dados_base = bloco.css("ul.itens li span::text").getall()
            # Normalmente retorna: ['x dormitórios', 'x m²', 'x vagas']
            dormitorios = None
            metragem = None
            vagas = None
            for txt in dados_base:
                if 'dormitório' in txt:
                    dormitorios = txt.split()[0]
                elif 'm²' in txt:
                    metragem = txt.split()[0]
                elif 'vaga' in txt:
                    vagas = txt.split()[0]
            
            # Extraindo o código do imóvel da URL
            if url_detalhes:
                codigo = url_detalhes.rstrip('/').split('/')[-1]  # Remove o / do final se existir e pega a última parte
            else:
                codigo = None
            
            dados_basicos = {
                "codigo": codigo,
                "url_detalhes": url_detalhes,
                "url_img": url_img,
                "preco": preco,
                "bairro": bairro,
                "cidade": cidade,
                "tipo": tipo,
                "dormitorios": dormitorios,
                "metragem": metragem,
                "vagas": vagas,
            }
            
            # Segue para página de detalhes (mantendo os dados já coletados)
            yield response.follow(
                url_detalhes,
                callback=self.parse_detail,
                meta={'dados_basicos': dados_basicos}
            )


        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        dados = response.meta['dados_basicos']
        
        # Campos detalhados
        endereco = ''.join(response.css('.tx-ficha span ::text').getall()).strip()
        descricao = response.css(".tx-ficha.mt-4 .tx::text").get()
        iptu = response.css(".box-side .valor ul li:nth-child(1)::text").get()
        condominio = response.css(".box-side .valor ul li:nth-child(2)::text").get()
        caracteristicas = response.css(".dts-imovel li::text").getall()
        
        # ...

        # Adicionando os dados detalhados ao dicionário
        dados['endereco'] = endereco
        dados['descricao'] = descricao
        dados['iptu'] = iptu
        dados['condominio'] = condominio
        dados['caracteristicas'] = caracteristicas

        # Salvar/exportar o item completo
        yield dados