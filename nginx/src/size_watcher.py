#!/usr/bin/env python3
import heapq
import os
import sys
import time
import daemon
import logging

from ekirill.common import file_is_free, get_logger
from ekirill.config import app_config


class SizeWatcher:
    def __init__(self, path: str, max_size_gb: float, full_recheck_every: int, logger):
        self._reset()
        self._path = path
        self._max_size_gb = max_size_gb
        self._full_recheck_every = full_recheck_every
        self._logger = logger

    @property
    def _size_in_gb(self) -> float:
        return round(self._size / 1024 / 1024 / 1024, 1)

    def _add_file(self, file_name):
        if file_name not in self._files:
            # new file should be added to heap
            self._files.add(file_name)

            file_size = os.path.getsize(file_name)
            file_ctime = time.ctime(os.path.getctime(file_name))
            heapq.heappush(self._heap, (file_ctime, file_name, file_size))
            self._size += file_size

            self._logger.debug(f'Added {file_name}, total size now is: {self._size_in_gb} Gb')

    def _remove_file(self):
        """
        Removes the oldest file
        """
        _, file_name, file_size = heapq.heappop(self._heap)
        self._logger.debug(f'Removing `{file_name}`')
        try:
            os.unlink(file_name)
            self._files.remove(file_name)
            self._size -= file_size
        except IOError as e:
            self._logger.warning(f'Failed, skipping: {e}')

    def _forget_files(self, file_names):
        new_heap = []
        for file_ctime, file_name, file_size in self._heap:
            if file_name in file_names:
                self._files.remove(file_name)
                self._size -= file_size
                self._logger.debug(f'File {file_name} disappeared, total size now is: {self._size_in_gb} Gb')
            else:
                new_heap.append((file_ctime, file_name, file_size))
        heapq.heapify(new_heap)
        self._heap = new_heap

    def _get_new_files(self):
        seen = set()
        for root, _, files in os.walk(self._path):
            for file in files:
                file_name = os.path.join(root, file)
                if file_is_free(file_name):
                    # if file is used by another process, it may being written right now, skipping
                    seen.add(file_name)
                    self._add_file(file_name)

        # if some files were removed externally, we should forget them
        dissapeared = self._files - seen
        if dissapeared:
            self._forget_files(dissapeared)

    def _clean(self):
        if self._size_in_gb > self._max_size_gb:
            self._logger.debug(f'Size exceeds {self._max_size_gb} Gb')
            while self._size_in_gb > self._max_size_gb and len(self._heap):
                self._remove_file()

    def _reset(self):
        self._last_recheck = time.time()
        self._heap = []
        self._files = set()
        self._size = 0

    def run(self):
        while True:
            if time.time() - self._last_recheck >= self._full_recheck_every:
                self._logger.debug('Time to full recheck.')
                self._reset()

            self._get_new_files()
            self._clean()
            time.sleep(60)


if __name__ == '__main__':
    with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        logger = get_logger('SizeWatcher', 'SIZE_WATCHER')

        logger.info(f'Start watching the storage. `{app_config.storage.dir}`')
        watcher = SizeWatcher(
            app_config.storage.dir,
            app_config.storage.max_size_gb,
            app_config.storage.full_recheck_every,
            logger=logger,
        )
        watcher.run()
