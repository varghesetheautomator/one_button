import logging
import time
import os


class Logger():

    def __init__(self, logger, file_level=logging.INFO):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fmt = logging.Formatter(
            '%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')

        curr_time = time.strftime("%Y-%m-%d")
        log_directory = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_directory, exist_ok=True)
        self.LogFileName = os.path.join(
            log_directory, 'log' + curr_time + '.txt')
        # "a" to append the logs in the same file, "w" to generate a new log file and delete the old one
        fh = logging.FileHandler(self.LogFileName, mode="a")
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(fh)
