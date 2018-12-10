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
from multiprocessing import Process, Queue
from cplex_server.controllers.allowed_flows import get_flows, get_allowed_flows

# dict: id: {status:status, bimatrix: [], imatrix: []}

class JobInfo():

    def __init__(self, id, status, data_file="", output_file=""):
        self._id = id
        self.status = JobStatus(id, status)
        self.data_file = data_file
        self.output_file = output_file

    def set_status(self, status):
        self.status = JobStatus(self._id, status)

    def set_output_file(self, output_file):
        self.output_file = output_file

    def __repr__(self):
        return "Status: %s Data File: %s Output File: %s" % (self.status.status, self.data_file, self.output_file)

JOBS = {4: JobInfo(4, "processing", "cs490.dat", "output.txt")}
curr_id = 0
queue = Queue()

def find_status_by_job_id(jobId):  # noqa: E501
    update_jobs()
    return JOBS[jobId].status # get status from job_status model


def get_bi_job_matrix(jobId):  # noqa: E501
    update_jobs()
    return parse_bi_job_matrix(JOBS[jobId].output_file)

def parse_bi_job_matrix(filename):
    with open(filename) as f:
        line = f.readline()
        line = f.readline()
        sp = line.split()
        sp[0] = sp[0][1:]
        sp[-1] = sp[-1][:1]
        return [int(i) for i in sp]

def get_i_matrix(jobId):  # noqa: E501
    update_jobs()
    return parse_i_matrix(JOBS[jobId].output_file)

def parse_i_matrix(filename):
    with open(filename) as f:
        line = f.readline() # BIJobs
        line = f.readline() # BIJobs matrix
        line = f.readline() # I line
        arr = []
        for line in f:
            if line.strip():
                arr.append(line.strip().split())
        arr[0][0] = arr[0][0][1:]
        arr[-1][-1] = arr[-1][-1][:1]

        for a in arr:
            a[0] = a[0][1:]
            a[-1] = a[-1][:1]
        return [[int(i) for i in a] for a in arr]

def update_jobs():
    while not queue.empty():
        top_id = queue.get()
        JOBS[top_id].set_status("done")
        JOBS[top_id].set_output_file("%d_output_file.txt" % top_id)


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

def write_to_data_file(body):
    global curr_id
    curr_id += 1
    filename = 'data_files/{id}_{date:%Y-%m-%d_%H-%M-%S}.dat'.format(id=curr_id, date=datetime.datetime.now())
    flows = get_flows(body.source_nodes, body.dest_nodes)
    with open(filename, 'w') as f:
        f.write('Flows = {')
        for flow in flows:
            f.write('"%s",' % flow)
        f.write("};\n")

        f.write('Jobs = {')
        for job in body.jobs:
            f.write('"%s",' % job)
        f.write("};\n")

        f.write("numConstraints = %d;\n" % body.num_constraints)

        f.write("A = %s;\n" % str(body.a))

        f.write("C = %s;\n" % str(body.c))
        
        allowed_flows = get_allowed_flows(flows)
        f.write("AllowedFlows = %s;\n" % str(allowed_flows))
        f.write("JobId = %s;\n" % curr_id)

    JOBS[curr_id] = JobInfo(curr_id, "processing", filename, "")
    print("added to job queue")
    p = Process(target=run_cplex_job, args=(filename, curr_id))
    p.start()
    return curr_id

def run_cplex_job(data_file, id_num):
    try:
        s = subprocess.check_output([return_cplex_loc(), return_model_loc(), data_file])
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    print(id_num)
    queue.put(id_num)

def return_cplex_loc():
    return '/home/anushreeagrawal/CPLEX_Studio128/opl/bin/x86-64_linux/oplrun'

def return_model_loc():
    return 'cs490.mod'


