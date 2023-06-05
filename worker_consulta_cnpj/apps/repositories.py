from os import getenv
import structlog
from email.mime.text import MIMEText


logger = structlog.get_logger()


class JobsSQLAlchemyRepository():
    def __init__(self, adapter) -> None:
        logger.info("update_status.job.sqlalchemy.repository", message="updated")

        self.adapter = adapter

    def update_status(self, job_id, new_status) -> None:
        try:
            sql = """ UPDATE job SET status = %s WHERE id = %s"""

            # create a new cursor
            self.adapter.connect()
            cur = self.adapter.cur
            # execute the UPDATE  statement
            cur.execute(sql, (new_status, job_id))
            updated_rows = cur.rowcount
            self.adapter.commit()

            logger.info("update_status.job.sqlalchemy.repository", updated_rows=updated_rows, message="updated")

        except Exception as err:
            raise err
        finally:
            self.adapter.close()

    def update_duration(self, job_id, duration) -> None:
        try:
            sql = """ UPDATE job SET duration = %s WHERE id = %s"""
            self.adapter.connect()
            cur = self.adapter.cur
            cur.execute(sql, (duration, job_id))
            updated_rows = cur.rowcount
            self.adapter.commit()

            logger.info("update_duration.job.sqlalchemy.repository", updated_rows=updated_rows, duration=duration, message="duration")

        except Exception as err:
            raise err
        finally:
            self.adapter.close()


class ResultSQLAlchemyRepository():
    def __init__(self, adapter) -> None:
        self.adapter = adapter

    def insert(self, data) -> None:
        try:
            sql = """
                INSERT INTO result(
                    job_id,
                    atividade_principal,
                    cnpj,
                    bairro,
                    cep,
                    complemento,
                    data_abertura,
                    data_pesquisa,
                    email,
                    hora_pesquisa,
                    logradouro,
                    matriz_filial,
                    municipio,
                    natureza_juridica,
                    nome_empresarial,
                    nome_fantasia,
                    numero,
                    porte,
                    telefone,
                    uf,
                    source,
                    creator_id,
                    creator_email
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            self.adapter.connect()
            cur = self.adapter.cur
            cur.execute(
                sql,
                (
                    data['job_id'],
                    data['atividade_principal'],
                    data['cnpj'],
                    data['bairro'],
                    data['cep'],
                    data['complemento'],
                    data['data_abertura'],
                    data['data_pesquisa'],
                    data['email'],
                    data['hora_pesquisa'],
                    data['logradouro'],
                    data['matriz_filial'],
                    data['municipio'],
                    data['natureza_juridica'],
                    data['nome_empresarial'],
                    data['nome_fantasia'],
                    data['numero'],
                    data['porte'],
                    data['telefone'],
                    data['uf'],
                    data['source'],
                    data['creator_id'],
                    data['creator_email'],
                )
            )
            updated_rows = cur.rowcount
            self.adapter.commit()
            logger.info("insert.result.sqlalchemy.repository", updated_rows=updated_rows, message="created")

        except Exception as err:
            raise err
        finally:
            self.adapter.close()


class EmailRepository:
    def __init__(self, adapter) -> None:
        self.adapter = adapter

    def start(self, job):
        try:
            msg = MIMEText(f"Hello, your  {job['id']} is in progess. Please check the app when you get a job done email")
            msg['Subject'] = f"Job {job['id']} is in progress"
            msg['From'] = 'no-reply-worker@consultacnpj.com'
            msg['To'] = job['creator_email']

            self.adapter.send(msg)
        except Exception as err:
            raise err

    def finish(self, job):
        try:
            msg = MIMEText(f"Hello, your  {job['id']} is in progess. Please check the app when you get a job done email")
            msg['Subject'] = f"Job {job['id']} is in progress"
            msg['From'] = 'no-reply-worker@consultacnpj.com'
            msg['To'] = job['creator_email']


            self.adapter.send(msg)
        except Exception as err:
            raise err

