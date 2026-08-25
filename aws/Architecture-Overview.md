# AWS Architecture Overview

## Objective

Provide a low-cost serverless platform capable of receiving workstation telemetry and displaying occupancy status in near real time.

## AWS Services

### API Gateway

Entry point for telemetry requests.

### Lambda

Business logic processing layer.

### DynamoDB

Persistent storage layer.

### CloudWatch

Monitoring and diagnostics.

## Benefits

- Serverless
- Pay-as-you-go
- Highly scalable
- Minimal infrastructure management
- Low operational cost

## Security

- HTTPS endpoints
- IAM permissions
- Principle of least privilege
- CloudWatch auditing
