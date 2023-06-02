import structlog

logger = structlog.get_logger()


class SolveHCaptcha:

    def execute(self):
        logger.info('Resolvendo o captcha')