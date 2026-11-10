# NetworkPolicy Context Optimization

Research project focused on optimizing network telemetry selection for LLM-assisted verification of Kubernetes NetworkPolicy configurations.

The project investigates how to select relevant network observations under a limited token budget while accounting for the coverage of executed communication scenarios.

## Technologies

- Kubernetes (Kind)
- Cilium
- Hubble
- OpenTelemetry Demo
- Python (planned)
- Large Language Models (planned)

## Current Status

The local Kubernetes environment has been deployed using Kind, Cilium, and Hubble.

A reduced OpenTelemetry Demo deployment is running successfully, providing microservice communication for network telemetry collection.

The implementation of controlled communication scenarios, NetworkPolicy configurations, and context selection algorithms is planned.

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

### Deploy OpenTelemetry Demo

The experimental environment uses a reduced deployment of OpenTelemetry Demo to provide communication between microservices.

The deployment includes three application services (`recommendation`, `product-catalog`, and `cart`), along with their supporting dependencies and observability components.

The built-in load generator is disabled to enable controlled execution of communication scenarios.

**Versions:**
- OpenTelemetry Demo: `3.1.0`
- Helm chart: `0.42.6`

Add the Helm repository:

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

Update the repository:

```bash
helm repo update
```

Install OpenTelemetry Demo:

```bash
helm install otel-demo open-telemetry/opentelemetry-demo --version 0.42.6 --namespace otel-demo --create-namespace --values infrastructure/otel_values.yaml
```

Verify the deployment:

```bash
kubectl get pods -n otel-demo
```

## Project Structure

```text
networkpolicy_context_optimization/
├── infrastructure/
│   ├── kind_config.yaml
│   ├── cilium_values.yaml
│   └── otel_values.yaml
├── .gitignore
├── LICENSE
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