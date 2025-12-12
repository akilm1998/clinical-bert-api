See README-local.md for detailed local development instructions.
# Clinical Assertion Negation BERT – Real-Time API

Production-ready FastAPI service exposing a ClinicalBERT-based model for assertion negation classification, packaged in Docker and deployed on Amazon ECS Fargate through a CI/CD pipeline (CircleCI).

## 🚀 Features

- Pretrained **Clinical Assertion Negation BERT** model for real-time inference  
- FastAPI server with `/health` and `/predict` endpoints  
- **Full CI/CD pipeline:**
  - Linting (**Black**, **Flake8**)
  - Unit tests (**Pytest**)
  - Build & push Docker image to **Amazon ECR**
  - Register new **ECS Task Definition**
  - Update **ECS Service** (includes manual approval gates)
- Production deployment on **AWS ECS Fargate** behind an ALB  
- Automated environment parity: same Docker image used in both dev and prod  
- Fully reproducible, deterministic Docker environment 

---

## About CI/CD (CircleCI)

This project uses **CircleCI** to provide a reproducible, audited CI/CD pipeline that builds, tests, pushes the Docker image to ECR, registers a new ECS task definition revision, and deploys the new revision to the ECS service. The pipeline is intentionally split into small, auditable steps with manual approvals at key points so reviewers can inspect artifacts before a production change is applied.

### Pipeline goals
- Run linting and unit tests on every push / PR.
- Build a Docker image and push an immutable, commit-tagged artifact to Amazon ECR.
- Register a new ECS task definition revision that references the exact image pushed by the pipeline.
- Update the ECS service to point to that new task-definition revision and wait for the service to stabilize.
- Keep deployment gates (approvals) between build, task registration, and service update to allow safe manual validation.


