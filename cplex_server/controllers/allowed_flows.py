def get_flows(source_nodes, dest_nodes):
    flows = []
    flow_index = 0
    for src in source_nodes:
        for dest in dest_nodes:
            flows.append(Flow(src, dest, flow_index))
            flow_index += 1

    return flows


def get_allowed_flows(flows):
    allowed_flows_matrix = []
    for flow1 in flows:
        row = []
        for flow2 in flows:
            if flow1 == flow2:
                row.append(1)
            elif flow1.src != flow2.src and flow1.dest != flow2.dest:
                row.append(1)
            else:
                row.append(0)
        allowed_flows_matrix.append(row)
    return allowed_flows_matrix


class Flow:
    def __init__(self, src, dest, id_num):
        self.src = src
        self.dest = dest
        self.id_num = id_num

    def __repr__(self):
        return self.src + "_" + self.dest + "_f" + str(self.id_num) 

if __name__ == "__main__":
    source_nodes = ["m1", "m2", "m3"]
    dest_nodes = ["n1", "n2", "n3"]
    flows = get_flows(source_nodes, dest_nodes)
    allowed_flows = get_allowed_flows(flows)

    print("flows:", flows)
    print("allowed_flows:")
    for row in allowed_flows:
        print(row)



