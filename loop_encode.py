# init logger
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

import sqsqueue
import ffmpeg
import json
import base64


def encode(message):
    logger.debug(message.body)
    try:
        body = base64.b64decode(message.body)
        data = json.loads(body.decode('utf-8'))
    except Exception as e:
        logger.exception(e)
        message.delete()
        return

    logger.debug(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': ')))

    (ipath, opath) = ffmpeg.transform_path(data["recorded"])
    ffmpeg.ffmpeg(ipath, opath)

    message.delete()

def main():
    sqsqueue.loop_queue(sqsqueue.get_queue("chinachu-encode"), encode)

if __name__ == "__main__":
    main()
