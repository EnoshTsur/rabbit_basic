# user
RABBIT_USER_NAME = 'enosh'
RABBIT_PASSWORD = '1234'

# vhost
RABBIT_VHOST = 'enosh_host'

#queues
ENOSH_QUEUE = 'enosh_queue'
DIRECT_QUEUE = 'direct_bind'
LOGS_INFO_QUEUE = 'log_info_queue'
LOGS_ERROR_QUEUE = 'log_error_queue'
LOGS_ALL_QUEUE = 'log_all_queue'

#routing keys
ROUTING_KEY = 'demonstrate'
LOG_INFO_ROUTING_KEY = 'log.info'
LOG_ERROR_ROUTING_KEY = 'log.error'
LOG_ALL_ROUTING_KEY = 'log.*'

#exchane
DIRECT_EXCHANGE = 'amq.direct'
TOPIC_EXCHANGE = 'amq.topic'