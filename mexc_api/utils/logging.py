import datetime
import sys

import loguru


class Logging:
    def __init__(self, save_logs: bool = False) -> int:
        _datetime = (
            datetime.datetime.now()
                             .replace(microsecond=0)
                             .isoformat(sep="_")
        )
        self.fmt = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level>\t| "
                "<level>{message}</level>"
            )
        self.config = {
            "handlers": [
                {"sink": sys.stderr, "format": self.fmt},
            ],
        }
        loguru.logger.configure(**self.config)
        if save_logs:
            loguru.logger.add(
                sink=f"./{_datetime}.log",
                format=self.fmt,
                enqueue=False,
                backtrace=False,
                catch=True,
            )

    def trace(mes: str) -> None:
        return loguru.logger.trace(__message=mes)

    def debug(mes: str) -> None:
        return loguru.logger.debug(mes)

    def info(self, mes: str) -> None:
        return loguru.logger.info(mes)

    def success(mes: str) -> None:
        return loguru.logger.success(mes)

    def warning(mes: str) -> None:
        return loguru.logger.warning(mes)

    def error(mes: str) -> None:
        return loguru.logger.error(mes)

    def critical(mes: str) -> None:
        return loguru.logger.critical(mes)

    def exception(mes: str) -> None:
        return loguru.logger.exception(mes)
