"""
Organize all API entrypoints
Author: Po-Chun, Lu

"""
from endpoints.qol.resource import QolJob

RESOURCES = {"/qol/jobs": QolJob}
