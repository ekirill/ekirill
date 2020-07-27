#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from typing import Set

import daemon

from ekirill.common import file_is_free, get_logger
from ekirill.config import app_config


class ThumbMaker:
    def __init__(self, path: str, ext: str, width, height: int, logger):
        self._path = path
        self._ext = ext
        self._width = width
        self._height = height
        self._broken = set()
        self._logger = logger

    def _get_new_files(self) -> Set:
        unthumbed = set()
        for root, _, files in os.walk(self._path):
            for file in files:
                if not file.endswith('.mp4'):
                    continue

                file_name = os.path.join(root, file)
                if not file_is_free(file_name):
                    # if file is used by another process, it may being written right now, skipping
                    continue

                thumb_filename = f'{file_name}.{self._ext}'
                if os.path.exists(thumb_filename):
                    continue

                unthumbed.add(file_name)

        return unthumbed

    def _make_thumbnails(self, files: Set[str]):
        for file_name in files:
            if file_name in self._broken:
                continue

            if os.path.exists(file_name):
                thumb_filename = f'{file_name}.{self._ext}'
                try:
                    result = subprocess.run(
                        [
                            'ffmpeg',
                            '-i', file_name,
                            '-vf',
                            f'thumbnail,scale={self._width}:{self._height}',
                            '-frames:v', '1',
                            thumb_filename
                        ],
                        capture_output=True,
                        check=False,
                    )
                    if result.returncode != 0:
                        self._logger.error(
                            "Error processing `%s`: %s \n %s",
                            file_name,
                            result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
                        )
                        self._broken.add(file_name)
                    else:
                        if os.path.exists(thumb_filename):
                            self._logger.info(f'Created {thumb_filename}')
                        else:
                            self._logger.info(f'Could not generate thumb for {file_name}. Dunno why.')
                            self._broken.add(file_name)
                except Exception as e:
                    self._logger.error("Error processing `%s`", file_name)
                    self._broken.add(file_name)

    def run(self):
        while True:
            new_files = self._get_new_files()
            self._make_thumbnails(new_files)
            time.sleep(60)


if __name__ == '__main__':
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        logger = get_logger('ThumbMaker', 'THUMB_MAKER')

        logger.info(f'Start making thumbs. `{app_config.storage.dir}`')
        maker = ThumbMaker(
            app_config.storage.dir,
            app_config.thumbnails.ext,
            app_config.thumbnails.width,
            app_config.thumbnails.height,
            logger=logger,
        )
        maker.run()
