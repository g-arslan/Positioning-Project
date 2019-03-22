import os
import subprocess
import logging
from math import sin, cos, sqrt, pi
from statistics import mean, variance

from django.conf import settings
from django.template.loader import render_to_string
from latex import build_pdf

from ..models import Result

CONFIG_FILE = 'config.ini'
RESULT_GGA_FILE = 'result.gga'
RESULT_CSV_FILE = 'result.csv'
RESULT_PDF_FILE = 'result.pdf'
PATH_TO_FILE_KEY = 'path'
RESULT_STORE_FOLDER_NAME = 'playground'

logger = logging.getLogger(__name__)

class FileProcessing:
    E2 = 0.00669437999014
    OME2 = 0.99330562000987
    A = 6378137.0

    DAY_LEN = 24 * 60 * 60

    GGA_LINE_TYPE = 0
    GGA_TIME = 1
    GGA_LAT = 2
    GGA_LAT_SIGN = 3
    GGA_LON = 4
    GGA_LON_SIGN = 5
    GGA_QUALITY = 6
    GGA_NUM_OF_SATS = 7
    GGA_HGT = 9
    GGA_GEOID_SEP = 11

    def convert_coordinates(self, lat, lon, hgt):
        slat = sin(lat)
        clat = cos(lat)
        slon = sin(lon)
        clon = cos(lon)

        n = self.A / sqrt(1. - self.E2 * slat * slat)
        nph = n + hgt
        x = nph * clat * clon
        y = nph * clat * slon
        z = (self.OME2 * n + hgt) * slat
        return (x, y, z)

    def parse_time(self, time):
        time = int(time)
        sec = time % 100
        time //= 100
        min = time % 100
        return time // 100 * 60 * 60 + min * 60 + sec

    def parse_coord(self, coord):
        coord = str(coord)
        left, right = coord.split('.')
        right = left[-2:] + '.' + right
        left = left[:-2]
        grad = float(left) + float(right) / 60.0
        return grad / 180.0 * pi

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

        # TODO: delete this
        with open(os.path.join(workdir, RESULT_GGA_FILE), 'w') as ggafile:
            ggafile.write(render_to_string('get_data_form/sample.gga'))

        data = []
        fx = []
        fy = []
        fz = []

        with open(os.path.join(workdir, RESULT_GGA_FILE), 'r') as ggafile:
            for line in ggafile:
                ggadata = line.split(',')
                if ggadata[self.GGA_LINE_TYPE] == '$GPGGA':
                    time = self.parse_time(float(ggadata[self.GGA_TIME]))
                    lat = self.parse_coord(ggadata[self.GGA_LAT])
                    if ggadata[self.GGA_LAT_SIGN] == 'S':
                        lat *= -1
                    lon = self.parse_coord(ggadata[self.GGA_LON])
                    if ggadata[self.GGA_LON_SIGN] == 'W':
                        lon *= -1
                    hgt = float(ggadata[self.GGA_HGT]) + float(ggadata[self.GGA_GEOID_SEP])
                    # print("{}, {}, {}".format(lat, lon, hgt))
                    x, y, z = self.convert_coordinates(lat, lon, hgt)
                    # print("{}, {}, {}".format(x, y, z))
                    sat_count = int(ggadata[self.GGA_NUM_OF_SATS])
                    data.append({'time': time, 'x': x, 'y': y, 'z': z, 'sat_count': sat_count})
                    if ggadata[self.GGA_QUALITY] == '5':
                        fx.append(x)
                        fy.append(y)
                        fz.append(z)

        days = 0

        xavg = mean(fx)
        xcov = variance(fx)
        yavg = mean(fy)
        ycov = variance(fy)
        zavg = mean(fz)
        zcov = variance(fz)
        x_min = min(map(lambda a: a['x'], data))
        x_max = max(map(lambda a: a['x'], data))
        y_min = min(map(lambda a: a['y'], data))
        y_max = max(map(lambda a: a['y'], data))
        z_min = min(map(lambda a: a['z'], data))
        z_max = max(map(lambda a: a['z'], data))

        for i in range(0, len(data)):
            data[i]['x'] = (data[i]['x'] - x_min) / (x_max - x_min)
            data[i]['y'] = (data[i]['y'] - y_min) / (y_max - y_min)
            data[i]['z'] = (data[i]['z'] - z_min) / (z_max - z_min)
            if i > 0:
                data[i]['time'] += days * self.DAY_LEN
                if data[i]['time'] <= data[i - 1]['time']:
                    days += 1
                    data[i]['time'] += self.DAY_LEN

        with open(os.path.join(workdir, RESULT_CSV_FILE), 'w') as csvfile:
            csvfile.write('Coordinate,E,COV\n')
            csvfile.write('X,{avg},{cov}\n'.format(avg=xavg, cov=xcov))
            csvfile.write('Y,{avg},{cov}\n'.format(avg=yavg, cov=ycov))
            csvfile.write('Z,{avg},{cov}\n'.format(avg=zavg, cov=zcov))

        with open(os.path.join(workdir, RESULT_PDF_FILE), 'wb') as pdffile:
            report = render_to_string('get_data_form/report.tex', {
                'data': data,
                'xavg': xavg,
                'xcov': xcov,
                'yavg': yavg,
                'ycov': ycov,
                'zavg': zavg,
                'zcov': zcov,
                'sat_min': min(map(lambda a: a['sat_count'], data)) - 1,
                'sat_max': max(map(lambda a: a['sat_count'], data)) + 1,
                'time_min': min(map(lambda a: a['time'], data)) - 1,
                'time_max': max(map(lambda a: a['time'], data)) + 1,
                'x_min': x_min,
                'x_max': x_max,
                'y_min': y_min,
                'y_max': y_max,
                'z_min': z_min,
                'z_max': z_max,
            })
            with open(os.path.join(workdir, 'report.tex'), 'w') as texfile:
                texfile.write(report)
            build_pdf(report).save_to(pdffile)

        instance.result_csv.name = os.path.join(RESULT_STORE_FOLDER_NAME, str(submission.id), RESULT_CSV_FILE)
        instance.result_pdf.name = os.path.join(RESULT_STORE_FOLDER_NAME, str(submission.id), RESULT_PDF_FILE)
        instance.status = Result.DONE
        instance.save()

        logger.info('Finished processing "{data_file}"'.format(data_file=submission.data_file.name))
