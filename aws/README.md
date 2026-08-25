
# AWS Components

Desk Telemetry uses AWS serverless services to receive, process, store, and display workstation telemetry data.

## Services Used

### API Gateway

Receives telemetry data from PowerShell agents running on Windows workstations.

Responsibilities:

- Expose HTTPS endpoints
- Receive telemetry requests
- Route requests to Lambda

---

### AWS Lambda

Processes telemetry events received from API Gateway.

Responsibilities:

- Validate requests
- Match workstation records
- Determine desk status
- Update DynamoDB

---

### DynamoDB

Stores workstation and desk information.

Example Data:

- Desk Code
- Hostname
- Monitor ID
- Employee Name
- Status
- Timestamp

---

### CloudWatch

Provides operational monitoring and troubleshooting.

Used For:

- Lambda Logs
- Error Tracking
- Performance Monitoring

---

## Solution Flow

Windows Endpoint
↓
PowerShell Agent
↓
API Gateway
↓
Lambda
↓
DynamoDB
↓
Dashboard

---

## Skills Demonstrated

- AWS Serverless Architecture
- API Integration
- DynamoDB Data Modeling
- Monitoring and Logging
- Cloud Operations
- Troubleshooting

---

## Future Enhancements

- Email Notifications
- Dashboard Hosting
- Scheduled Reporting
- Metrics and Analytics
