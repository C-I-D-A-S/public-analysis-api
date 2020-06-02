"""
Endpoint Module for handling spark triggering
Author: Po-Chun, Lu

"""
import uuid
import threading
from datetime import datetime, timedelta

from flask_restful import Resource, reqparse
from flask import current_app as app

from endpoints.qol.args import add_post_args
from endpoints.qol.msg_queue import send_kafka_msg
from endpoints.utils import log_context


def get_kafka_msg(args):
    """ generate kafka msg queue msg based on arguments
    """
    job_id = str(uuid.uuid4())

    return (
        job_id,
        {
            "username": args.username,
            "job_type": args.job_type,
            "job_id": job_id,
            "job_config": {
                "request_time": datetime.strftime(
                    (datetime.now()), app.config["DATE_TIME"]
                ),
                "deadline": datetime.strftime(
                    (datetime.now() + timedelta(seconds=args.deadline)),
                    app.config["DATE_TIME"],
                ),
            },
            "job_parameters": args.job_parameters,
        },
    )


class QolJob(Resource):
    """ /qol/jobs handler

    """

    def __init__(self):
        self.model = None
        self._set_post_parser()

    def _set_post_parser(self):
        self.post_parser = reqparse.RequestParser()
        add_post_args(self.post_parser)

    @staticmethod
    def _prod_msg(topic, job_id, kafka_msg):
        send_kafka_msg(topic, job_id, kafka_msg)

    def _execute_thread(self, args):
        job_id, kafka_msg = get_kafka_msg(args)
        log_context("Request", {"kafka_msg": kafka_msg})

        if app.config["IS_MULTI_THREAD"]:
            threading.Thread(
                target=self._prod_msg, args=(app.config["TOPIC"], job_id, kafka_msg)
            ).start()
        else:
            self._prod_msg(app.config["TOPIC"], job_id, kafka_msg)

        return job_id

    def _post_operate(self, args):
        return self._execute_thread(args)

    def post(self):
        """ main handler of post request """
        args = self.post_parser.parse_args()
        job_id = self._post_operate(args)

        return {"path": f"/qol/jobs/{job_id}", "ETA": 180}
