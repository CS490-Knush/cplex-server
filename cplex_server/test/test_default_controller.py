# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from cplex_server.models.bi_job_matrix import BIJobMatrix  # noqa: E501
from cplex_server.models.i_matrix import IMatrix  # noqa: E501
from cplex_server.models.job_status import JobStatus  # noqa: E501
from cplex_server.models.parameters import Parameters  # noqa: E501
from cplex_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_find_status_by_job_id(self):
        """Test case for find_status_by_job_id

        Finds job status for id
        """
        response = self.client.open(
            '/cpsc490/cplex_server/1.0.0/status/{jobId}'.format(jobId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_bi_job_matrix(self):
        """Test case for get_bi_job_matrix

        Returns BIJob matrix for job with id
        """
        response = self.client.open(
            '/cpsc490/cplex_server/1.0.0/bijobmatrix/{jobId}'.format(jobId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_i_matrix(self):
        """Test case for get_i_matrix

        Returns I matrix for job with id
        """
        response = self.client.open(
            '/cpsc490/cplex_server/1.0.0/imatrix/{jobId}'.format(jobId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_submit_job(self):
        """Test case for submit_job

        Submit json for cplex to optimize job
        """
        body = Parameters()
        response = self.client.open(
            '/cpsc490/cplex_server/1.0.0/optimize',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
