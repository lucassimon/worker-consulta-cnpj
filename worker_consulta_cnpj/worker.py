import time
import os
import json
import pika
import structlog
from datetime import datetime
from dotenv import load_dotenv

from adapters.postgres import PostgresAdapter
from adapters.smtp import SmtpLibAdapter
from apps.scraper import ScrapperPlaywright


queue_name = 'job_created'
logger = structlog.get_logger()
load_dotenv(dotenv_path='./.env')


def callback(ch, method, properties, body):
    try:
        start_duration = datetime.now()
        message = body.decode()
        job = json.loads(message)

        postgres_adapter = PostgresAdapter(
            host=os.getenv("POSTGRES_HOST"),
            db=os.getenv("POSTGRES_DB"),
            username=os.getenv("POSTGRES_USERNAME"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )

        smtp_adapter = SmtpLibAdapter(host='localhost', port=1025)

        scrapper = ScrapperPlaywright(
            db_adapter=postgres_adapter,
            smtp_adapter=smtp_adapter,
            job=job,
            start_duration=start_duration
        )
        scrapper.run()

        print(" [x] Received %r" % job)
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as err:
        logger.exception("An error occurred!", err=err)
        # If requeue is true, the server will attempt to
        # requeue the message. If requeue is false or the
        # requeue attempt fails the messages are discarded or
        # dead-lettered.
        ch.basic_nack(requeue=False)

def get_channel():
    # connect and get channel
    parameters = pika.URLParameters('amqp://guest:guest@localhost:5672')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # declare queue with max priority
    arguments = {
        "x-dead-letter-exchange": 'create-job-use-case-dlq',
        "x-dead-letter-routing-key": 'job_created_dlq',
        "x-max-priority": 5
    }
    channel.queue_declare(
        queue=queue_name, durable=True, arguments=arguments
    )
    channel.basic_qos(prefetch_count=1)
    return channel


if __name__ == '__main__':

    channel = get_channel()

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()

