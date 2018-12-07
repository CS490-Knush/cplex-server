import connexion
import six
import json
import datetime
import subprocess

from cplex_server.models.bi_job_matrix import BIJobMatrix  # noqa: E501
from cplex_server.models.i_matrix import IMatrix  # noqa: E501
from cplex_server.models.job_status import JobStatus  # noqa: E501
from cplex_server.models.parameters import Parameters  # noqa: E501
from cplex_server import util
from multiprocessing import Process

# dict: id: {status:status, bimatrix: [], imatrix: []}

class JobInfo():


    def __init__(self, id, status, data_file="", output_file=""):
        self.status = JobStatus(id, status)
        self.data_file = data_file
        self.output_file = output_file

JOBS = {4: JobInfo(4, "processing", "cs490.dat", "output.txt")}
curr_id = 0

def find_status_by_job_id(jobId):  # noqa: E501
    return JOBS[jobId].status # get status from job_status model


def get_bi_job_matrix(jobId):  # noqa: E501
    return JOBS[jobId]['bijobmatrix']


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
        new_id = write_to_data_file(body)
        return new_id

    return 'do some magic!'

def write_to_data_file(body):
    global curr_id
    curr_id += 1
    global JOBS
    filename = 'data_files/{id}_{date:%Y-%m-%d_%H-%M-%S}.dat'.format(id=curr_id, date=datetime.datetime.now())
    with open(filename, 'w') as f:
        f.write('Flows = {')
        for flow in body.flows:
            f.write('"%s",' % flow)
        f.write("};\n")

        f.write('Jobs = {')
        for job in body.jobs:
            f.write('"%s",' % job)
        f.write("};\n")

        f.write("numConstraints = %d;\n" % body.num_constraints)

        f.write("A = %s;\n" % str(body.a))

        f.write("C = %s;\n" % str(body.c))
        
        allowed_flows = [[1, 1, 0, 0],
               [1, 1, 0, 0],
               [0, 0, 1, 1],
               [0, 0, 1, 1]]
        f.write("AllowedFlows = %s;\n" % str(allowed_flows))

    JOBS[curr_id] = JobInfo(curr_id, "processing", filename, "")
    print("added to job queue")
    p = Process(target=run_cplex_job, args=(filename, curr_id))
    p.start()
    return curr_id

def run_cplex_job(data_file, curr_id):
    try:
        s = subprocess.check_output([return_cplex_loc(), return_model_loc(), data_file])
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    print(s)
    JOBS[curr_id].status = "done"
    JOBS[curr_id].data_file = "output_files/%d_output_file.txt" % curr_id

def return_cplex_loc():
    return '/home/anushreeagrawal/CPLEX_Studio128/opl/bin/x86-64_linux/oplrun'

def return_model_loc():
    return 'cs490.mod'


