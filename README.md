# NetworkPolicy Context Optimization

Research project focused on optimizing network telemetry selection for LLM-assisted verification of Kubernetes NetworkPolicy configurations.

The proposed method combines policy-aware filtering, microservice dependency analysis, and telemetry aggregation to select relevant network context under a limited token budget.

## Technologies

- Kubernetes (kind)
- Cilium and Hubble
- OpenTelemetry Demo
- Python
- Large Language Models (planned)

## Current Status

A local Kubernetes environment has been deployed using kind, Cilium, and Hubble.

A reduced OpenTelemetry Demo deployment is running with selected microservices and supporting components.

Three functional communication scenarios (F1–F3) have been implemented and tested. Their NetworkPolicy configurations were validated through controlled blocking and restoration of network communication, with results observed in Hubble.

Initial Python-based telemetry analysis is available. Experiment automation, the proposed context selection algorithm, and LLM integration are planned.

## Infrastructure

The local Kubernetes cluster consists of:

- 1 control-plane node
- 2 worker nodes
- Cilium 1.20.4
- Hubble Relay and Hubble UI

Configuration files are available in `infrastructure/`.

### Create the Kubernetes Cluster

```bash
kind create cluster --name networkpolicy-lab --config infrastructure/kind_config.yaml
```

### Install Cilium and Hubble

```bash
helm repo add cilium https://helm.cilium.io/
helm repo update
helm install cilium cilium/cilium --version 1.20.4 --namespace kube-system --values infrastructure/cilium_values.yaml
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

The environment uses a reduced OpenTelemetry Demo deployment with three application services (`recommendation`, `product-catalog`, and `cart`) and their supporting dependencies.

The built-in load generator is disabled to enable controlled experiments.

**Versions:**
- OpenTelemetry Demo: `3.1.0`
- Helm chart: `0.42.6`

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm install otel-demo open-telemetry/opentelemetry-demo --version 0.42.6 --namespace otel-demo --create-namespace --values infrastructure/otel_values.yaml
kubectl get pods -n otel-demo
```

## Functional Scenarios

Three communication dependencies have been tested:

| Scenario | Dependency | NetworkPolicy direction |
|---|---|---|
| F1 | `recommendation → product-catalog` (TCP/8080) | Ingress |
| F2 | `product-catalog → astronomy-db` (TCP/5432) | Egress |
| F3 | `cart → valkey-cart` (TCP/6379) | Egress |

Each scenario was verified by blocking and restoring the required connection, observing application behavior and Hubble network flows.

Scenario definitions are available in `scenarios/`, and NetworkPolicy manifests in `networkpolicies/`.

## Project Structure

```text
networkpolicy_context_optimization/
├── infrastructure/
│   ├── cilium_values.yaml
│   ├── kind_config.yaml
│   └── otel_values.yaml
├── networkpolicies/
│   ├── f1_allow_recommendation.yaml
│   ├── f1_isolate_product_catalog_ingress.yaml
│   ├── f2_allow_astronomy_db.yaml
│   ├── f2_allow_auxiliary_egress.yaml
│   ├── f3_allow_auxiliary_egress.yaml
│   └── f3_allow_valkey_cart.yaml
├── scenarios/
│   └── functional_scenarios.yaml
├── src/
│   └── analyze_flows.py
├── pyproject.toml
├── .python-version
├── .gitignore
├── LICENSE
└── README.md
```

## Research Scope

The research focuses on:

1. Policy-aware and dependency-aware telemetry selection.
2. Reducing redundant network observations.
3. Optimizing context selection under a limited token budget.
4. Evaluating LLM-based NetworkPolicy verification across correct, missing, excessive, and mixed configurations.

**Next steps:** Automate experimental data collection, implement the context selection algorithm, and evaluate it against baseline methods.

## Acknowledgments

This project uses [OpenTelemetry Demo](https://github.com/open-telemetry/opentelemetry-demo), an open-source microservice application developed by the OpenTelemetry community, as its experimental environment.

OpenTelemetry Demo is licensed under the [Apache License 2.0](https://github.com/open-telemetry/opentelemetry-demo/blob/main/LICENSE).