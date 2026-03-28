---
title: Cloud-Ops OpenEnv
emoji: ☁️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Cloud-Ops Incident Responder

A high-utility SRE environment for evaluating AI agents on infrastructure recovery.

## Domain Motivation

Simulates critical failure scenarios—service crashes, memory leaks, and database deadlocks—that require deterministic logic to resolve.

## Environment Specification

### Observation Space

The agent receives a JSON object containing:

- `logs`: Standard output strings from the service.
- `cpu_usage`: Float (0.0 - 100.0).
- `memory_usage`: Float (0.0 - 100.0).
- `active_alerts`: List of error codes.
- `step_count`: Integer tracking episode length.

### Action Space

The agent must submit an Action object:

- `command`: The action (RESTART, SCALE_UP, KILL_SESSIONS).
- `target`: The service (auth-service, payment-api, db-cluster).

---

## Tasks and Baseline Scores

| Task ID | Name | Difficulty | Score |
| :--- | :--- | :--- | :--- |
| task_1 | Service Recovery | Easy | 1.0 |
| task_2 | Memory Mitigation | Medium | 1.0 |
| task_3 | Database Deadlock Fix | Hard | 1.0 |

---

## Setup and Usage

1. **Local Development**:
   `pip install -r requirements.txt`
   `uvicorn main:app --port 7860`

## Baseline Script

Included as `baseline.py`. Run this to reproduce 1.0 scores across all tasks.