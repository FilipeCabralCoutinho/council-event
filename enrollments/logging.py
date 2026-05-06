import logging
import sys
from logging.handlers import RotatingFileHandler

from rich import print as rprint
from rich.markdown import Markdown


class CustomActionHandler(logging.Handler):
    def emit(self, record):
        """
        Método acionado quando o log atinge os requisitos do Handler.
        Insira aqui a lógica da sua ação.
        """
        try:
            from enrollments.models import LogReport
            
            new_log = LogReport(
                levelname=record.levelname,
                name=record.name,
                message=record.getMessage(),
                filename=record.filename,
                lineno=record.lineno
            )
            new_log.save()
        except Exception:
            self.handleError(record)

def setup_logging():
    # config root logger
    stream_handler_root = logging.StreamHandler(sys.stdout)
    stream_handler_root.setFormatter(
        logging.Formatter(fmt="ROOT: [ %(levelname)s ] %(message)s ")
    )
    logging.basicConfig(handlers=[stream_handler_root])

    # config my logger
    logger = logging.getLogger("app_enrollment")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(asctime)s | %(message)s | %(filename)s | %(lineno)d"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler(
        "app_enrollment.log", maxBytes=10485760, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # config custom handler para WARNING, ERROR e CRITICAL
    custom_action_handler = CustomActionHandler()
    custom_action_handler.setLevel(logging.WARNING) # Pega WARNING, ERROR e CRITICAL
    custom_action_handler.setFormatter(formatter)
    logger.addHandler(custom_action_handler)

    md = Markdown("# Logger App Enrollment ")
    rprint(md)

    return logger


logger = setup_logging()