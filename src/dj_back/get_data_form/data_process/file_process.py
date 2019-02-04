import os
from shutil import copy
import subprocess
import logging

from django.conf import settings
from django.core.files import File

from ..models import Result

CONFIG_FILE = 'config.ini'
PATH_TO_FILE_KEY = 'path'
RESULT_FILENAME = 'result.txt'
RESULT_STORE_FOLDER_NAME = 'playground'

logger = logging.getLogger(__name__)

class FileProcessing:
    def process_file(self, submission):
        workdir = os.path.join(settings.MEDIA_ROOT, RESULT_STORE_FOLDER_NAME, str(submission.id))
        os.makedirs(workdir)

        copy(os.path.join(settings.BIN_ROOT, CONFIG_FILE), workdir)
        config = open(os.path.join(workdir, CONFIG_FILE), 'a')
        config.write('\n{key}={value}\n'.format(
            key=PATH_TO_FILE_KEY,
            value=os.path.join(workdir, os.path.basename(submission.data_file.name)),
        ))
        config.close()

        os.symlink(os.path.join(settings.BIN_ROOT, settings.PROCESS_NAME), os.path.join(workdir, settings.PROCESS_NAME))
        os.symlink(os.path.join(settings.MEDIA_ROOT, submission.data_file.name),
                   os.path.join(workdir, os.path.basename(submission.data_file.name)),
        )

        result = subprocess.run(
            [os.path.join(workdir, settings.PROCESS_NAME)],
            universal_newlines=True,
            cwd=workdir,
        )

        if result.returncode != 0:
            logger.error('Failure while parsing file {filename}, exit code is {exitcode}, stderr: {stderr}'.format(
                filename=submission.data_file.name,
                exitcode=result.returncode,
                stderr=result.stderr,
            ))
            return

        instance = Result()
        instance.submission = submission
        instance.result_file.name = os.path.join(RESULT_STORE_FOLDER_NAME, str(submission.id), RESULT_FILENAME)
        instance.save()

        logger.info('Finished processing "{data_file}"'.format(data_file=submission.data_file.name))
