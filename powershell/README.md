# PowerShell Components

This folder contains the PowerShell scripts that power the Desk Telemetry solution.

## Overview

Desk Telemetry uses PowerShell to collect workstation telemetry data, detect monitor connectivity, identify active devices, and provide real-time occupancy reporting through AWS serverless services.

The solution was designed to help organizations gain visibility into workspace utilization without requiring additional hardware.

---

## Components

### sent-telemetry.ps1

Primary telemetry collection agent.

Responsibilities:

- Detect workstation hostname
- Identify connected external monitors
- Generate unique monitor identifiers
- Build telemetry payloads
- Send data to AWS API Gateway
- Log successful and failed transmissions

Collected Data:

- Computer Name
- Monitor Identifier
- Timestamp
- Agent Version

Key Technologies:

- CIM / WMI
- JSON Serialization
- REST APIs
- PowerShell Logging
- Error Handling

---

### MonitorWatcher.ps1

Background monitoring service.

Responsibilities:

- Continuously monitor workstation status
- Detect monitor connection events
- Detect monitor disconnection events
- Trigger telemetry updates
- Keep desk occupancy information current

Key Technologies:

- PowerShell Loops
- Windows Event Monitoring
- Automation Workflows

---

### see-current-status.ps1

Real-time monitoring dashboard.

Responsibilities:

- Retrieve workstation status from AWS
- Display current desk occupancy
- Highlight inactive or unassigned desks
- Refresh automatically every 15 seconds

Status Indicators:

| Status | Description |
|----------|----------|
| OK | Desk assigned and reporting normally |
| NO_MONITOR | Device online without external monitor |
| UNASSIGNED_DEVICE | Device not assigned to a desk |
| NO_REPORT | No recent telemetry received |

---

## Solution Workflow

```text
Windows Workstation
        ↓
Agent.ps1
        ↓
AWS API Gateway
        ↓
AWS Lambda
        ↓
DynamoDB
        ↓
Dashboard.ps1
```

---

## Skills Demonstrated

- PowerShell Scripting
- Systems Monitoring
- Windows Administration
- Endpoint Management
- REST API Integration
- Event-Based Automation
- Troubleshooting
- Technical Documentation
- AWS Integration
- Operational Monitoring

---

## Real-World Use Case

This project was developed as a practical workspace monitoring solution capable of identifying:

- Occupied desks
- Available desks
- Devices without monitors
- Devices not assigned to users
- Workstation activity status

The information can be used to improve asset visibility and workspace utilization reporting.

---

## Future Enhancements

- Multi-monitor support
- Historical reporting
- Automated notifications
- CloudWatch integration improvements
- Enhanced dashboard visualization
- Reporting analytics
