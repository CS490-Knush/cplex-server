# Benchmark Cplex
import sys
import time
import requests
import json

def request_generator(num_m, num_n):
    sourceNodes = []
    destNodes = []
    jobs = []
    for i in range(num_m):
        sourceNodes.append("m%d" % i)
    for i in range(num_n):
        destNodes.append("n%d" % i)
    for i in range(num_n + num_m):
        jobs.append("j%d" % i)
    num_flows = num_m + num_n
    A1 = [1]
    A1.extend([0] * (num_flows-1))
    A2 = [0, 1]
    A2.extend([0] * (num_flows-2))
    A3 = [0, 0, 1]
    A3.extend([0] * (num_flows-3))
    A4 = [0, 0, 0, 1]
    A4.extend([0] * (num_flows-4))
    A5 = [0, 0, 1, 1]
    A5.extend([0] * (num_flows-4))
    A = [A1, A2, A3, A4, A5]

    C = [4, 5, 2, 6, 7]

    data = {"sourceNodes": sourceNodes,
            "destNodes": destNodes,
            "jobs": jobs,
            "numConstraints": 5,
            "A": A,
            "C": C}
    print(data)
    send_request(num_flows, num_flows, data)

def send_request(computation_nodes, storage_nodes, cplex_request):
    start_time = time.time()
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://localhost:8080/cpsc490/cplex_server/1.0.0/optimize', data=json.dumps(cplex_request), headers=headers)
    if r.status_code == 200:
        print("Successful optimization")
    job_code = int(r.json())
    print(job_code)
    bimatrix = []
    while bimatrix == []:
        r = requests.get('http://localhost:8080/cpsc490/cplex_server/1.0.0/status/%d' % job_code)
        if r.status_code != 200:
            print("error getting job status...")
            return
        if r.json()['status'] != 'done':
            time.sleep(1)
            continue
        bimatrix_req = requests.get('http://localhost:8080/cpsc490/cplex_server/1.0.0/bijobmatrix/%d' % job_code)
        if bimatrix_req.status_code == 200:
            end_time = time.time()
            write_to_csv(computation_nodes, storage_nodes, end_time-start_time)

def write_to_csv(computation_nodes, storage_nodes, time):
    filename = sys.argv[1]
    with open(filename, 'a') as f:
        f.write("%s,%s,%s\n" % (computation_nodes, storage_nodes, str(time)))

def main():
    filename = sys.argv[1]
    with open(filename, 'a') as f:
        f.write("Computation Nodes,Storage Nodes,Time\n")
    for i in range(2, 6):
        for b in range(2, 6):
            request_generator(i, b)

if __name__ == "__main__":
    main()
