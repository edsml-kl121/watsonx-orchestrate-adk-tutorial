podman buildx build --platform linux/amd64 -t th-new-agentic-hr .
podman tag th-new-agentic-hr u1800085/ibm-student-image:th-new-agentic-hr
podman push u1800085/ibm-student-image:th-new-agentic-hr