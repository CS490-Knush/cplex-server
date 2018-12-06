# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from cplex_server.models.base_model_ import Model
from cplex_server import util


class JobStatus(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, job_id: int=None, status: str=None):  # noqa: E501
        """JobStatus - a model defined in Swagger

        :param job_id: The job_id of this JobStatus.  # noqa: E501
        :type job_id: int
        :param status: The status of this JobStatus.  # noqa: E501
        :type status: str
        """
        self.swagger_types = {
            'job_id': int,
            'status': str
        }

        self.attribute_map = {
            'job_id': 'jobId',
            'status': 'status'
        }

        self._job_id = job_id
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'JobStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The JobStatus of this JobStatus.  # noqa: E501
        :rtype: JobStatus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def job_id(self) -> int:
        """Gets the job_id of this JobStatus.


        :return: The job_id of this JobStatus.
        :rtype: int
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id: int):
        """Sets the job_id of this JobStatus.


        :param job_id: The job_id of this JobStatus.
        :type job_id: int
        """
        if job_id is None:
            raise ValueError("Invalid value for `job_id`, must not be `None`")  # noqa: E501

        self._job_id = job_id

    @property
    def status(self) -> str:
        """Gets the status of this JobStatus.


        :return: The status of this JobStatus.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this JobStatus.


        :param status: The status of this JobStatus.
        :type status: str
        """
        allowed_values = ["processing", "done", "not found"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status
