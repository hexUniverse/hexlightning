import sys
import time
import logging
import argparse

import pymongo
from pymongo.errors import ConnectionFailure
from termcolor import colored
from configparser import ConfigParser


# Custom
import handle
from plugin import emojitags


class app:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.txt', encoding='utf8')
        self.run_mode = vars(args)['mode']
        self.loggingFormat = f'{colored("%(asctime)s", "white")} - !name - {colored("%(levelname)s", "red")} - %(message)s'
        self.client = pymongo.MongoClient(self.config.get('database', 'url'))
        self.emojitags = emojitags
        file_handler = logging.FileHandler(filename='hexlightning.log')
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging_handler = [file_handler, stdout_handler]
        if self.run_mode == 'debug':
            # 2018-10-25 16:22:04,046 - __main__ - DEBUG - Debugging
            loggingFormat = self.loggingFormat.replace(
                '!name', colored("%(name)s", "red"))
            logging.basicConfig(
                level=logging.DEBUG,
                format=loggingFormat,
                handlers=logging_handler
            )
            self.logger = logging.getLogger(__name__)
            self.logger.debug('Debugging')
        else:
            loggingFormat = self.loggingFormat.replace(
                '!name', colored("%(name)s", "cyan"))
            logging.basicConfig(
                level=logging.INFO,
                format=loggingFormat,
                handlers=logging_handler
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info('Initializing...')

    def run(self):
        try:
            self.logger.info(
                f'Connecting to mongo@{self.config.get("database", "url")}')
            self.client.admin.command('ismaster')
            self.client = self.client.hexlightning
            self.logger.info('Connectd to DB')
        except KeyboardInterrupt:
            print('\nExit;')
        except ConnectionFailure:
            self.logger.critical('DB DOWN...!!')
            # sys.exit()
        else:
            self.logger.info('Listening...')
        finally:
            handle.worker(
                inherit=self,
                token=self.config.get('bot', 'token'),
            )
        # self.logger.info('\nExit.')ˋ


ansciiArtHex = '''
██╗  ██╗███████╗██╗  ██╗⚡️
██║  ██║██╔════╝╚██╗██╔╝
███████║█████╗   ╚███╔╝
██╔══██║██╔══╝   ██╔██╗
██║  ██║███████╗██╔╝ ██╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

'''
ansciiArtName = '''
██╗     ██╗ ██████╗ ██╗  ██╗████████╗███╗   ██╗██╗███╗   ██╗ ██████╗
██║     ██║██╔════╝ ██║  ██║╚══██╔══╝████╗  ██║██║████╗  ██║██╔════╝
██║     ██║██║  ███╗███████║   ██║   ██╔██╗ ██║██║██╔██╗ ██║██║  ███╗
██║     ██║██║   ██║██╔══██║   ██║   ██║╚██╗██║██║██║╚██╗██║██║   ██║
███████╗██║╚██████╔╝██║  ██║   ██║   ██║ ╚████║██║██║ ╚████║╚██████╔╝
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝

'''

print(colored(ansciiArtHex, 'cyan'), colored(ansciiArtName, 'yellow'))
tmp = f'{time.strftime("%Y/%m/%d %H:%M:%S %Z")}\n' \
      f'Version: v1.0'
print(tmp)

parser = argparse.ArgumentParser(description='hexPort Product.')
parser.add_argument('mode',
                    nargs='?',
                    default='run',
                    choices=['run', 'debug', 'test'],
                    help='Select bot run mode')

args = parser.parse_args()
if __name__ == '__main__':
    app = app()
    try:
        app.run()
    except Exception as e:
        app.logger.exception(e)
