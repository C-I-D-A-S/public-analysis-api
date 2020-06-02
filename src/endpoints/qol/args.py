"""
Module for API arguments config
Author: Po-Chun, Lu

"""


def add_post_args(post_parser):
    """ defining post arguments
    """
    post_parser.add_argument(
        "username",
        type=str,
        required=True,
        location="headers",
        help="username parameter should be str",
    )

    post_parser.add_argument(
        "job_type",
        type=str,
        required=True,
        location="json",
        help="job_type parameter should be str",
    )

    post_parser.add_argument(
        "deadline",
        type=int,
        required=True,
        location="json",
        help="deadline parameter should be int",
    )

    post_parser.add_argument(
        "job_parameters",
        type=dict,
        required=True,
        location="json",
        help="job_parameters should be dict",
    )
