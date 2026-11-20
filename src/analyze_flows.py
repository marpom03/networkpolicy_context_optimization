import json
import sys
from collections import Counter


def get_pod_name(endpoint):

    workloads = endpoint.get("workloads", [])

    if workloads:
        return workloads[0]["name"]

    pod_name = endpoint.get("pod_name")

    if pod_name:
        return pod_name

    labels = endpoint.get("labels", [])

    for label in labels:
        if label.startswith("reserved:"):
            return label

    return "unknown"


def analyze_flows(file_path):
    connections = Counter()

    with open(file_path, "r") as file:
        for line in file:
            record = json.loads(line)
            flow = record.get("flow", {})

            if flow.get("is_reply", False):
                continue

            source = get_pod_name(flow.get("source", {}))
            destination = get_pod_name(flow.get("destination", {}))

            l4 = flow.get("l4", {})

            if "TCP" in l4:
                protocol = "TCP"
            elif "UDP" in l4:
                protocol = "UDP"
            else:
                continue

            port = l4[protocol].get("destination_port")
            verdict = flow.get("verdict", "UNKNOWN")

            key = (source, destination, protocol, port, verdict)
            connections[key] += 1

    return connections


if __name__ == "__main__":
    file_path = sys.argv[1]
    results = analyze_flows(file_path)

    print(
        f"{'SOURCE':<25} {'DESTINATION':<25} {'PROTOCOL':<10} {'PORT':<8} {'VERDICT':<12} COUNT"
    )
    print("-" * 95)

    for (source, destination, protocol, port, verdict), count in sorted(
        results.items()
    ):
        print(
            f"{source:<25} {destination:<25} {protocol:<10} {port!s:<8} {verdict:<12} {count}"
        )
