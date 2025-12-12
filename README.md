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
## Model loading & caching (loaded once at startup)

To keep inference fast and avoid re-loading the heavy ClinicalBERT model for every request, the model is **loaded once at process startup** and reused for all incoming requests. This both reduces latency and prevents excessive memory/CPU churn when the API receives concurrent requests. Here we use **lru_cache**
---

## About CI/CD (CircleCI)

This project uses **CircleCI** to provide a reproducible, audited CI/CD pipeline that builds, tests, pushes the Docker image to ECR, registers a new ECS task definition revision, and deploys the new revision to the ECS service. The pipeline is intentionally split into small, auditable steps with manual approvals at key points so reviewers can inspect artifacts before a production change is applied.

### Pipeline goals
- Run linting and unit tests on every push / PR.
- Build a Docker image and push an immutable, commit-tagged artifact to Amazon ECR.
- Register a new ECS task definition revision that references the exact image pushed by the pipeline.
- Update the ECS service to point to that new task-definition revision and wait for the service to stabilize.
- Keep deployment gates (approvals) between build, task registration, and service update to allow safe manual validation.

---

## About OIDC roles, security, and CircleCI contexts

### Why we use OIDC (short)
We use **OIDC-based short-lived credentials** instead of long-lived AWS access keys. CircleCI can request a short-lived token from AWS by assuming an IAM Role through OIDC (web identity). This removes long-lived secrets from CircleCI, reduces blast radius, and fits modern best-practices for CI → cloud authentication.


### Example trust policy (conceptual)
Use this pattern to trust CircleCI's OIDC provider and restrict which `sub` or `aud` claims may assume the role. The exact provider ARN may differ — follow CircleCI docs to obtain the correct provider URL.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Federated": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:oidc-provider/<circleci-oidc-provider>" },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<circleci-oidc-provider>:sub": "repo:YOUR_ORG/YOUR_REPO:ref:refs/heads/*"
        }
      }
    }
  ]
}
```

CircleCI contexts & environment variables (recommended)
Store configuration values and secrets in CircleCI Contexts (team-level protected variables). Example variables you should set in a secure context (e.g., aws):

AWS_REGION (e.g. us-east-1)

AWS_ORG_ACCOUNT (account id used for ECR URI)

Access control: only grant the CircleCI Context to projects that need it and to specific teams/users.

How the pipeline uses the role (practical)
The pipeline calls the orb aws-cli/setup with role_arn (or uses the orb auth param).

aws-cli/setup handles OIDC token exchange under the hood and writes temporary AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN into the environment for the job.

All later orb commands (aws-ecr/build_and_push_image, aws-ecs/update_task_definition, aws-ecs/deploy_service_update, etc.) run with those temporary creds.

Security best-practices & operational notes
No long-lived AWS keys in repo or contexts. Use OIDC role instead.

Least privilege: restrict the OIDC role to only the actions required by CI. Add iam:PassRole only for the specific task role ARNs.

Tighten trust condition in the IAM role to the specific CircleCI repo (or branch patterns) rather than allowing any repo.

Audit & logging: enable CloudTrail and monitor assume-role events. Tag deployments (task definition tags) for traceability.

Secrets for runtime: store runtime secrets in AWS Secrets Manager or Parameter Store and reference them via the task definition (do not bake secrets into images or repo).

Context access policy: limit which teams/projects can use the CircleCI context that contains ROLE_ARN.

Immutable image tags: always tag Docker images with commit SHA (${CIRCLE_SHA1}) to ensure reproducible deploys and easy rollbacks.

Rotate and review: periodically review attached policies and rotate/adjust permissions as the pipeline evolves.

Example CircleCI context variables to create
Create a CircleCI context named aws and set:

AWS_REGION
AWS_ORG_ACCOUNT 





