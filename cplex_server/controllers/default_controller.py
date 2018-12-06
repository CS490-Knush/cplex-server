import connexion
import six

from cplex_server.models.bi_job_matrix import BIJobMatrix  # noqa: E501
from cplex_server.models.i_matrix import IMatrix  # noqa: E501
from cplex_server.models.job_status import JobStatus  # noqa: E501
from cplex_server.models.parameters import Parameters  # noqa: E501
from cplex_server import util


def find_status_by_job_id(jobId):  # noqa: E501
    """Finds job status for id

     # noqa: E501

    :param jobId: ID of job to return status for
    :type jobId: int

    :rtype: JobStatus
    """
    return 'do some magic!'


def get_bi_job_matrix(jobId):  # noqa: E501
    """Returns BIJob matrix for job with id

     # noqa: E501

    :param jobId: ID of job to return status for
    :type jobId: int

    :rtype: BIJobMatrix
    """
    return 'do some magic!'


def get_i_matrix(jobId):  # noqa: E501
    """Returns I matrix for job with id

     # noqa: E501

    :param jobId: ID of job to return status for
    :type jobId: int

    :rtype: IMatrix
    """
    return 'do some magic!'


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
