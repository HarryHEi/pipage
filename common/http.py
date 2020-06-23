import requests

from .logger import logger


def sync_get(*args, **kwargs):
    """Sync GET，尝试3次"""
    for i in range(3):
        try:
            res = requests.get(*args, **kwargs)
        except Exception as e:
            logger.error(e)
        else:
            if res.status_code // 100 == 2:
                return res

        logger.info(f'Try to get for {i+1} times failed.')

    logger.info(f'Give up get {args} {kwargs}')


def sync_download(url, filename):
    """下载文件，尝试3次"""
    for i in range(3):
        try:
            res = requests.get(url, stream=True)
        except Exception as e:
            logger.error(e)
        else:
            if res.status_code // 100 == 2:
                with open(filename, 'wb') as f:
                    for trunk in res.iter_content(1024):
                        f.write(trunk)
                logger.info(f'Download {url} successfully.')
                return
            else:
                logger.error(res.text)

        logger.error(f'Try to download from {url} for {i+1} times filed.')

    logger.error(f'Download {url} filed.')
