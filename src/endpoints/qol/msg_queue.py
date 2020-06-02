"""
Module for Sending Kafka msg
Author: Po-Chun, Lu

"""
import json

from loguru import logger

from kafka import PRODUCER


def _delivery_callback(err, msg):
    if err:
        logger.warning(f"Message failed delivery: {err}\n")
    else:
        logger.info(
            f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}\n"
        )


def send_kafka_msg(topic, job_id, kafka_msg):
    """ send kafka msg with msg key and msg value """

    logger.info(kafka_msg)

    try:
        PRODUCER.produce(
            topic=topic,
            key=job_id,
            value=json.dumps(kafka_msg),
            callback=_delivery_callback,
        )

    except BufferError:
        logger.warning(
            f"Local producer queue is full {len(PRODUCER)} messages awaiting delivery): try again\n"
        )

    PRODUCER.poll(0)

    # # Wait until all messages have been delivered
    logger.info(f"Waiting for {len(PRODUCER)} deliveries\n")
    PRODUCER.flush()
