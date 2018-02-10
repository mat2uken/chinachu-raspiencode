import sys
import boto3
import multiprocessing

# init logger
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

sqs = boto3.resource("sqs")

def get_queue(name="chinachu-encode"):
    queue = None
    try:
        queue = sqs.get_queue_by_name(QueueName="chinachu-encode")
        logger.debug("got logger: {}".format(queue))
    except Exception as e:
        logger.exception("Error: {}".format(e))
        sys.exit(-1)
    return queue

def loop_queue(queue, func=None):
    if func is None:
        def f(message): return (True, None)
        func = f

    while 1:
        msg_list = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=20)
        if not msg_list:
            logger.debug("got blank msg_list: {}".format(msg_list))
            continue

        for message in msg_list:
            p = multiprocessing.Process(target=func, args=(message,))
            p.start()
            p.join()

def main():
    def f(message):
        logger.debug("msg: {}".format(message))
        message.delete()
        return (True, None)
    loop_queue(get_queue("chinachu-encode"), f)

if __name__ == "__main__":
    main()
