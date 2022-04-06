import logging

# Logging with no output file
logging.basicConfig(format='%(asctime)s: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p',
                    handlers=[logging.StreamHandler()],
                    level=logging.INFO)

# Logging with output file
logging_file_path = r'log.txt'
logging.basicConfig(format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p',
                    handlers=[logging.FileHandler(
                        logging_file_path, mode='w'), logging.StreamHandler()],
                    level=logging.INFO)
