FROM docker.io/frappe/bench:latest

# Install socat and netcat for port forwarding (required for Antigravity devcontainer connection)
USER root
RUN apt-get update && apt-get install -y socat netcat-openbsd && rm -rf /var/lib/apt/lists/*
USER frappe
