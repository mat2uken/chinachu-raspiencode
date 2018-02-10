import os
import sys
import subprocess

# init logger
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

import json

def transform_path(recorded_path):
    input_filepath = recorded_path.replace("/data", "/mnt/nexboxa1")
    logger.debug("recorded filepath: {}".format(input_filepath))
    output_filepath = recorded_path.replace("/data", "/mnt/nexboxa1").replace("/recorded", "/transcoded")
    root, ext = os.path.splitext(output_filepath)
    output_filepath = root + ".mp4"
    logger.debug("input, output => ({}, {})".format(input_filepath, output_filepath))
    return (input_filepath, output_filepath)

def ffmpeg(input_filename, output_filename):
    res = subprocess.run(["ffmpeg", "-y", "-i", "{}".format(input_filename),
                          "-fflags", "+discardcorrupt", "-c:v", "mpeg2_mmal",
                          "-c:a", "copy", "-bsf:a", "aac_adtstoasc",
                          "-c:v", "h264_omx", "-b:v", "5000k",
                          "{}".format(output_filename)
                         ])
    logger.debug(res)

def main():
    with open("sample-program.json", "r") as f:
        try:
            data = json.load(f)
            logger.debug(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))
        except json.JSONDecodeError as e:
            logger.exception(e)

    (input_filepath, output_filepath) = transform_path(data["recorded"])
    ffmpeg(input_filepath, output_filepath)

if __name__ == "__main__":
    main()
