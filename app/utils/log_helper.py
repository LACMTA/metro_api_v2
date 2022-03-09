import logging
import logging.config

logger = logging.getLogger('uvicorn.app')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'logzioFormat': {
#             'format': '{"message": "%(message)s", "app": "api.metro.net"}',
#             'validate': False
#         }
#     },
#     'handlers': {
#         'logzio': {
#             'class': 'logzio.handler.LogzioHandler',
#             'level': 'INFO',
#             'formatter': 'logzioFormat',
#             'token': 'kEDlRQQyVfOhPgBmUlWgCaoFcBZUFYTh',
#             'logzio_type': 'fastapi',
#             'logs_drain_timeout': 5,
#             'url': 'https://listener.logz.io:8071'
#         }
#     },
#     'loggers': {
#         'app_logger': {
#             'level': 'INFO',
#             'handlers': ['logzio'],
#             'propagate': True
#         }
#     }
# }

# logging.config.dictConfig(LOGGING)
# logger = logging.getLogger('app_logger')
