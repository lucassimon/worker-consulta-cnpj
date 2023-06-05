import typing
# import time
from datetime import datetime
# from playwright.sync_api import sync_playwright
import structlog
from apps.hcaptcha import SolveHCaptcha
from apps.parser import ParseSiteReceita
from apps.repositories import JobsSQLAlchemyRepository, ResultSQLAlchemyRepository, EmailRepository

# import hcaptcha_challenger as solver
# from hcaptcha_challenger import HolyChallenger
# from hcaptcha_challenger.exceptions import ChallengePassed


logger = structlog.get_logger()
# Init local-side of the ModelHub
# solver.install()




class SiteReceita:
    def __init__(self) -> None:
        self.target = 'https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp'
        self.xpath_cnpj = 'xpath=//*[@id="cnpj"]'
        self.xpath_submit = 'xpath=//*[@id="frmConsulta"]/div[3]/div/button[1]'
        self.xpath_captcha = ''


class ScrapperPlaywright:

    def __init__(self, db_adapter, smtp_adapter,job, site = SiteReceita, parser = ParseSiteReceita, start_duration = None) -> None:
        self.db_adapter = db_adapter
        self.smtp_adapter = smtp_adapter
        self.job = job

        self.job_id = job['id']
        self.cnpj = job['cpf_cnpj']
        self.site = site()
        self.parser = parser()
        self.captcha = SolveHCaptcha()
        self.start_duration = start_duration

    def duration(self):
        later = datetime.now()
        return (later - self.start_duration).total_seconds()

    def run(self):
        repo_results = ResultSQLAlchemyRepository(adapter=self.db_adapter)
        repo_jobs = JobsSQLAlchemyRepository(adapter=self.db_adapter)
        repo_email = EmailRepository(adapter=self.smtp_adapter)

        repo_jobs.update_status(self.job_id, 'processing')
        repo_email.start(job=self.job)

        try:
            # with sync_playwright() as p:
            logger.info('inicializando o playwright')
            # browser = p.chromium.launch(headless=False)
            logger.info('browser chromium criado')
            # tab = browser.new_page()
            logger.info('criando uma pagina vazia')
            # tab.goto(self.target)
            logger.info(f'abrindo o site {self.site.target}')
            # tab.fill(self.xpath_cnpj, cnpj)
            logger.info('preechendo o campo cnpj')

            self.captcha.execute()

            # tab.locator(self.xpath_submit).click()


            # challenger = solver.new_challenger(screenshot=True, debug=True)
            # Replace selenium.webdriver.Chrome with CTX
            # ctx = solver.get_challenge_ctx(silence=False)
            # ctx.get("https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/Cnpjreva_Solicitacao.asp")
            # hit_challenge(ctx=ctx, challenger=challenger)


            logger.info('Enviando requisição clicando no campo submit')

            data = self.parser.execute(local=True, page=None)
            data.update({
                'job_id': self.job_id,
                'creator_id': self.job['creator_id'],
                'creator_email': self.job['creator_email']
            })

            repo_results.insert(data=data)

            repo_jobs.update_status(self.job_id, 'processed')
            difference = self.duration()
            repo_jobs.update_duration(self.job_id, difference)
            repo_email.finish(job=self.job)

        except Exception as err:
            repo_jobs.update_status(self.job_id, 'error')
            raise err


