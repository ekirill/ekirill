import psutil


def file_is_free(fpath):
    # if any process has file handle opened for this file, than it is not free
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return False
        except Exception:
            pass

    return True
