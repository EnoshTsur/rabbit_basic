from pika import PlainCredentials, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.connection import ConnectionParameters
from toolz import pipe

from app.settings.config import RABBIT_USER_NAME, RABBIT_PASSWORD, RABBIT_VHOST


def create_channel() -> BlockingChannel:
    return pipe(
        PlainCredentials(RABBIT_USER_NAME, RABBIT_PASSWORD),
        lambda credentials: ConnectionParameters(
            credentials=credentials,
            virtual_host=RABBIT_VHOST
        ),
        BlockingConnection,
        lambda connection: connection.channel()
    )
