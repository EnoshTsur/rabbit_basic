from app.rabbit.exchange import LogLevel
from app.rabbit.publish import publish_log

if __name__ == '__main__':
    publish_log("Hello enosh!", LogLevel.INFO)
