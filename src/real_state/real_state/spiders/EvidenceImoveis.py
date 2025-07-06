import scrapy

class EvidenceimoveisSpider(scrapy.Spider):
    name = "EvidenceImoveis"
    allowed_domains = ["www.evidenceimoveis.com.br"]
    start_urls = ["https://www.evidenceimoveis.com.br/busca/comprar/cidade/sao-paulo/bairros/analia-franco/categoria/apartamento/valor_de/250000/valor_ate/1500000/dormitorios/2/vagas/1/suites/1/area/70/1/"]

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
            yield {
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

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)