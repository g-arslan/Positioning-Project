import os
import subprocess
import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.core.files import File

from ..models import Result

CONFIG_FILE = 'config.ini'
PATH_TO_FILE_KEY = 'path'
RESULT_STORE_FOLDER_NAME = 'playground'

logger = logging.getLogger(__name__)

class FileProcessing:
    def process_file(self, submission, instance):
        workdir = os.path.join(settings.MEDIA_ROOT, RESULT_STORE_FOLDER_NAME, str(submission.id))
        os.makedirs(workdir)

        config = {}
        config['RoverFile'] = os.path.basename(submission.data_file.name)
        # config['RoverFile'] = os.path.join(workdir, os.path.basename(submission.data_file.name))
        config['OutputDir'] = '.'
        config['RoverAntID'] = submission.antenna

        with open(os.path.join(workdir, CONFIG_FILE), 'w') as configfile:
            configfile.write(render_to_string('get_data_form/default.ini', config))

        os.symlink(os.path.join(settings.BIN_ROOT, settings.PROCESS_NAME), os.path.join(workdir, settings.PROCESS_NAME))
        os.symlink(os.path.join(settings.MEDIA_ROOT, submission.data_file.name),
                   os.path.join(workdir, os.path.basename(submission.data_file.name)),
        )

        result = subprocess.run(
            [os.path.join(workdir, settings.PROCESS_NAME), CONFIG_FILE],
            universal_newlines=True,
            cwd=workdir,
        )

        if result.returncode != 0:
            instance.status = Result.ERROR
            instance.save()
            logger.error('Failure while parsing file {filename}, exit code is {exitcode}, stderr: {stderr}'.format(
                filename=submission.data_file.name,
                exitcode=result.returncode,
                stderr=result.stderr,
            ))
            return

        instance.result_csv.name = os.path.join(RESULT_STORE_FOLDER_NAME, str(submission.id), "result.csv")
        instance.result_pdf.name = os.path.join(RESULT_STORE_FOLDER_NAME, str(submission.id), "result.pdf")
        instance.status = Result.DONE
        instance.save()

        logger.info('Finished processing "{data_file}"'.format(data_file=submission.data_file.name))
