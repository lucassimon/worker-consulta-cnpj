import structlog
from lxml import html
import pathlib

logger = structlog.get_logger()


class ParseSiteReceita:

    def __init__(self) -> None:
        pass

    def get_cnpj(self, tree):
        cnpj = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[1]/font[2]/b[1]/text()')
        return cnpj[0]

    def get_matriz_filial(self, tree):
        matriz_filial = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[1]/font[2]/b[2]/text()')
        return matriz_filial[0]

    def get_data_abertura(self, tree):
        data_abertura = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[3]/font[2]/b/text()')
        return data_abertura[0]

    def get_nome_empresarial(self, tree):
        nome_empresarial = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[3]/tbody/tr/td/font[2]/b/text()')
        return nome_empresarial[0].strip()

    def get_nome_fantasia(self, tree):
        nome_fantasia = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[4]/tbody/tr/td[1]/font[2]/b/text()')
        return nome_fantasia[0].strip()

    def get_porte(self, tree):
        porte = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[4]/tbody/tr/td[3]/font[2]/b/text()')
        return porte[0]

    def get_atividade_principal(self, tree):
        atividade_principal = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[5]/tbody/tr/td/font[2]/b/text()')
        return atividade_principal[0].strip()

    def get_atividade_secundaria(self, tree):
        atividades = []
        td = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[6]/tbody/tr/td')[0]
        for fonts in td.getchildren():
            children = fonts.getchildren()
            for i, data in enumerate(children):
                atividades.append(data.text.strip())

        return atividades

    def get_natureza_juridica(self, tree):
        natureza_juridica = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[7]/tbody/tr/td/font[2]/b/text()')
        return natureza_juridica[0].strip()

    def get_logradouro(self, tree):
        logradouro = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[8]/tbody/tr/td[1]/font[2]/b/text()')
        return logradouro[0].strip()

    def get_numero(self, tree):
        numero = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[8]/tbody/tr/td[3]/font[2]/b/text()')
        return numero[0].strip()

    def get_complemento(self, tree):
        complemento = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[8]/tbody/tr/td[5]/font[2]/b/text()')
        return complemento[0].strip()

    def get_cep(self, tree):
        cep = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[9]/tbody/tr/td[1]/font[2]/b/text()')
        return cep[0].strip()

    def get_bairro(self, tree):
        bairro = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[9]/tbody/tr/td[3]/font[2]/b/text()')
        return bairro[0].strip()

    def get_municipio(self, tree):
        municipio = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[9]/tbody/tr/td[5]/font[2]/b/text()')
        return municipio[0].strip()

    def get_email(self, tree):
        email = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[10]/tbody/tr/td[1]/font[2]/b/text()')
        return email[0].strip()

    def get_uf(self, tree):
        uf = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[9]/tbody/tr/td[7]/font[2]/b/text()')
        return uf[0].strip()

    def get_telefone(self, tree):
        telefone = tree.xpath('//*[@id="principal"]/table[1]/tbody/tr/td/table[10]/tbody/tr/td[3]/font[2]/b/text()')
        return telefone[0].strip()

    def get_data_pesquisa(self, tree):
        data_pesquisa = tree.xpath('//*[@id="principal"]/table[2]/tbody/tr/td[1]/p/font/b[1]/text()')
        return data_pesquisa[0].strip()

    def get_hora_pesquisa(self, tree):
        hora_pesquisa = tree.xpath('//*[@id="principal"]/table[2]/tbody/tr/td[1]/p/font/b[2]/text()')
        return hora_pesquisa[0].strip()

    def parse_all(self, tree):
        return {
            "cnpj": self.get_cnpj(tree),
            "matriz_filial": self.get_matriz_filial(tree),
            "data_abertura": self.get_data_abertura(tree),
            "nome_empresarial": self.get_nome_empresarial(tree),
            "nome_fantasia": self.get_nome_fantasia(tree),
            "porte": self.get_porte(tree),
            "atividade_principal": self.get_atividade_principal(tree),
            "atividades_secundarias": self.get_atividade_secundaria(tree),
            "natureza_juridica": self.get_natureza_juridica(tree),
            "logradouro": self.get_logradouro(tree),
            "numero": self.get_numero(tree),
            "complemento": self.get_complemento(tree),
            "cep": self.get_cep(tree),
            "bairro": self.get_bairro(tree),
            "municipio": self.get_municipio(tree),
            "uf": self.get_uf(tree),
            "email": self.get_email(tree),
            "telefone": self.get_telefone(tree),
            "data_pesquisa": self.get_data_pesquisa(tree),
            "hora_pesquisa": self.get_hora_pesquisa(tree)
        }

    def parse_local_example(self):
        current_dir = pathlib.Path().resolve()
        file_path = current_dir / "static/screenshot-test-purposes.html"

        with open(file_path , "r", encoding="utf8") as f:
            page = f.read()
        return page

    def execute(self, local=True, page=None):
        logger.info('Parseando os dados do html com lxml')
        data = {}

        if local:
            page = self.parse_local_example()

        tree = html.fromstring(page)

        logger.info('Iniciando o parse')
        data = self.parse_all(tree)
        logger.info('Enviando requisição clicando no campo submit', data=data)

        return data
