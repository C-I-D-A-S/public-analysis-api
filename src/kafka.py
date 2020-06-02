"""
Kafka producer instance outside app context
Author: Po-Chun, Lu
"""

import os

from dotenv import load_dotenv
from loguru import logger
from confluent_kafka import Producer

load_dotenv()


def get_producer():
    """ init kafka producer instance """
    kafka_ip = os.environ.get("KAFKA_IP", "localhost:9092")
    group_id = os.environ.get("GROUP_ID", "qol")
    logger.info(f"KAFKA_IP {kafka_ip}, GROUP_ID {group_id}")

    conf = {
        "bootstrap.servers": kafka_ip,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "session.timeout.ms": 6000,
    }

    return Producer(**conf)


PRODUCER = get_producer()
