# NetworkPolicy Context Optimization

Research project focused on optimizing network telemetry selection for LLM-assisted verification of Kubernetes NetworkPolicy configurations.

The project investigates how to select relevant network observations under a limited token budget while accounting for the coverage of executed communication scenarios.

## Technologies

- Kubernetes (Kind)
- Cilium
- Hubble
- OpenTelemetry Demo (planned)
- Python (planned)
- Large Language Models (planned)

## Current Status

The initial Kubernetes infrastructure has been deployed locally using Kind, Cilium, and Hubble.

The implementation of traffic scenarios, NetworkPolicy configurations, and context selection algorithms is planned.

## Infrastructure

The local Kubernetes cluster consists of:

- 1 control-plane node
- 2 worker nodes
- Cilium 1.20.4
- Hubble Relay and Hubble UI

Configuration files are available in the `infrastructure/` directory.

### Create the Kubernetes Cluster

```bash
kind create cluster --name networkpolicy-lab --config infrastructure/kind_config.yaml
```

### Install Cilium and Hubble

Add the Helm repository:

```bash
helm repo add cilium https://helm.cilium.io/
```

Update the repository:

```bash
helm repo update
```

Install Cilium using the saved configuration:

```bash
helm install cilium cilium/cilium --version 1.20.4 --namespace kube-system --values infrastructure/cilium_values.yaml
```

Verify the installation:

```bash
cilium status --wait
```

### Access Hubble UI

```bash
cilium hubble ui
```

### Observe Network Flows

```bash
hubble observe -P --last 20
```

## Project Structure

```text
networkpolicy_context_optimization/
├── infrastructure/
│   ├── kind_config.yaml
│   └── cilium_values.yaml
├── .gitignore
└── README.md
```

## Research Scope

The planned research focuses on:

1. Policy-aware selection of relevant network telemetry.
2. Context selection under a fixed token budget.
3. Accounting for executed and unexecuted communication scenarios.
4. Evaluating LLM-based detection of excessive NetworkPolicy permissions.

## Development Status

Work in progress.
