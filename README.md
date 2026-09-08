# Orinfra SentinelOps

**Agentic Causal Investigation & Safe Remediation Platform for Production AI Systems**

Orinfra SentinelOps is an engineering platform designed to investigate
production incidents across data, machine-learning models, AI agents,
applications, infrastructure, and security systems.

The platform correlates distributed evidence, reconstructs probable
causal chains, estimates blast radius, and produces evidence-backed
remediation recommendations.

## Core Principle

> LLMs investigate evidence; they do not manufacture evidence.

Every investigation must be traceable to observable evidence.

When available evidence is insufficient to establish a reliable
conclusion, the system must be able to return:

`INSUFFICIENT_EVIDENCE`

## Project Status

Early engineering phase.

The project is currently establishing its repository, architecture,
testing, and development foundations.

## Planned Capabilities

- Production telemetry ingestion
- Anomaly detection
- Cross-system event correlation
- Evidence graph construction
- Specialized investigation agents
- Causal root-cause analysis
- Incident blast-radius estimation
- Historical incident retrieval
- Safe remediation recommendations
- Human approval workflows
- Incident simulation with known ground truth
- Automated evaluation of investigation quality
- MCP-based tool integration
- Observability and auditability

## Engineering Principles

- Evidence before inference
- Deterministic systems before probabilistic systems
- Explicit interfaces between components
- Human approval for consequential remediation
- Reproducible evaluation
- Security by design
- Measurable claims only