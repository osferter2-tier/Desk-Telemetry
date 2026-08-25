
# Solution Architecture

Desk Telemetry is built using PowerShell and AWS serverless services.

## Architecture Flow

```text
Windows Workstation
        ↓
Agent.ps1
        ↓
API Gateway
        ↓
AWS Lambda
        ↓
DynamoDB
        ↓
Dashboard
```

## AWS Components

### API Gateway

Receives telemetry data from workstations.

### Lambda

Validates and processes telemetry events.

### DynamoDB

Stores desk assignments and workstation status.

### Dashboard

Displays real-time occupancy information.

## Benefits

- Serverless architecture
- Low operational cost
- Near real-time visibility
- Minimal endpoint footprint
- Scalable design
```
