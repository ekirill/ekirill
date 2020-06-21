#!/usr/bin/env python
import heapq
import os
import time

import daemon

from ekirill.config import app_config


class SizeWatcher:
    def __init__(self, path: str, max_size_gb: int):
        self._heap = []
        self._files = set()
        self._size = 0
        self._path = path
        self._max_size_gb = max_size_gb

    @property
    def _size_in_gb(self) -> float:
        return round(self._size / 1024 / 1024 / 1024, 1)

    def get_new_files(self):
        for root, _, files in os.walk(self._path):
            for file in files:
                file_name = os.path.join(root, file)
                if file_name not in self._files:
                    self._files.add(file_name)

                    file_size = os.path.getsize(file_name)
                    file_ctime = time.ctime(os.path.getctime(file_name))
                    heapq.heappush(self._heap, (file_ctime, file_name, file_size))
                    self._size += file_size

                    print(f'Added {file_name}, total size now is: {self._size_in_gb} Gb')

    def clean(self):
        if self._size_in_gb > self._max_size_gb:
            print(f'Size exceeds {self._max_size_gb} Gb')
            while self._size_in_gb > self._max_size_gb and len(self._heap):
                _, file_name, file_size = heapq.heappop(self._heap)
                print(f'Removing `{file_name}`')
                try:
                    # os.unlink(file_name)
                    self._size -= file_size
                except IOError as e:
                    print(f'Failed, skipping: {e}')

    def run(self):
        while True:
            self.get_new_files()
            self.clean()
            time.sleep(10)


if __name__ == '__main__':
    with daemon.DaemonContext():
        watcher = SizeWatcher(app_config.camera.videodir, app_config.camera.max_size_gb)
        watcher.run()
