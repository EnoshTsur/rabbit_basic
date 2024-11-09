from app.rabbit.publish import publish_topic
from app.settings.config import LOG_INFO_ROUTING_KEY

if __name__ == '__main__':
    publish_topic("Hello topic!", routing_key=LOG_INFO_ROUTING_KEY)
