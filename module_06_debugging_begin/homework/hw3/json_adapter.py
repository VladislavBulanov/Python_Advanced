import logging
import json


class JsonAdapter(logging.LoggerAdapter):
    """The class for create an instance of LoggerAdapter
    initialized with an underlying Logger instance
    and a dict-like object."""

    def process(self, message, kwargs):
        """
        Modifies the message and/or keyword arguments
        passed to a logging call in order to insert
        contextual information.
        :param message: source message
        :param kwargs: kwargs
        :return: JSON-message
        """
        json_message = json.dumps(message)
        return json_message, kwargs


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('skillbox_json_messages.log')
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}',
        datefmt='%H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger = JsonAdapter(logger)

    logger.info('Сообщение')
    logger.error('Кавычка)"')
    logger.debug("Еще одно сообщение")
