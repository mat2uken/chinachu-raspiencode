#!/bin/sh

body=`echo $2 | /usr/bin/base64`

/usr/bin/aws sqs send-message \
    --queue-url https://ap-northeast-1.queue.amazonaws.com/482713154519/chinachu-encode \
    --message-body "${body}"
