import connexion
import six

from cplex_server.models.bi_job_matrix import BIJobMatrix  # noqa: E501
from cplex_server.models.i_matrix import IMatrix  # noqa: E501
from cplex_server.models.job_status import JobStatus  # noqa: E501
from cplex_server.models.parameters import Parameters  # noqa: E501
from cplex_server import util

# dict: id: {status:status, bimatrix: [], imatrix: []}
JOBS = {4: {'status': 'processing', 'bimatrix': [7, 8], 'imatrix': [[1, 0],[0, 1], [0, 0], [0,0]]}}

def find_status_by_job_id(jobId):  # noqa: E501
    return JOBS[jobId]['status']


def get_bi_job_matrix(jobId):  # noqa: E501
    return JOBS[jobId]['bimatrix']


def get_i_matrix(jobId):  # noqa: E501
    return JOBS[jobId]['imatrix']


def submit_job(body):  # noqa: E501
    """Submit json for cplex to optimize job

     # noqa: E501

    :param body: Parameters for cplex to optimize with
    :type body: dict | bytes

    :rtype: int
    """
    if connexion.request.is_json:
        body = Parameters.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
