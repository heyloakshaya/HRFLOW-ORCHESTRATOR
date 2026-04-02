HR processes such as hiring, onboarding, leave approvals, and employee relations are often handled across multiple disconnected systems. These workflows are mostly manual, time-consuming, and prone to errors, leading to inefficiencies, inconsistent decisions, and poor scalability.

Key challenges:
Fragmented systems with no central orchestration
Manual approvals and lack of automation
No intelligent decision-making
High operational overhead for HR teams
Limited visibility into workflows


HRFlow is an Agentic AI-powered HR workflow orchestration system built using IIL and MuleSoft API-led connectivity. It automates and manages employee lifecycle processes including hiring, leave management, onboarding, and employee relations.

The system integrates multiple microservices and uses AI agents to make intelligent decisions, reducing manual effort and improving efficiency.

Architecture Overview
The system follows an end-to-end flow:

User sends request (UI / Postman)
MuleSoft Experience API (Port 8081) receives request
Request is routed to Process Layer (AI orchestrator)
AI agent performs reasoning (Tool Call → Execute → Observe → Decide)
System APIs are invoked (Hiring, Leave, Relations, DB Layer)
Data is stored/retrieved from MySQL database
Final decision is generated (Approve / Reject / Escalate)
Notifications are sent via SMTP email

API-Led Connectivity
The application follows MuleSoft’s API-led architecture:

Experience Layer (Port 8081)
Handles client interaction
Authentication and authorization
Routes requests

Endpoints:

/api/login
/api/employee/*
/api/hr/*
Process Layer (Orchestration + AI)
Implements business logic
Executes AI reasoning loops
Coordinates between services
System Layer APIs
Hiring API (8086): Resume screening and interview scheduling
Leave API (8082): AI-based leave decision engine
Relations API (8084): Complaint handling
DB Layer API (8083): Internal database access (not exposed externally)

Agentic AI Design
The system uses an Agentic AI pattern:

Tool Call → Execute → Observe → Decide

AI Agents:

Hiring Agent (ATS evaluation)
Leave Decision Agent
Relations Agent
Resignation Analysis Agent

Examples:

Resume vs Job Description → AI score → Shortlist/Reject
Leave request → Context analysis → Risk-based decision

APIs & Endpoints
Authentication

POST /api/login

Employee APIs

GET /api/employee/interviews
GET /api/employee/team-leaves
POST /api/employee/apply-leave

HR APIs

GET /api/hr/candidates
GET /api/hr/leave-requests
GET /api/hr/interviews
POST /api/hr/approve-leave
POST /api/hr/reject-leave

Hiring API

POST :8086/hiring

Leave API

POST :8082/api/leave

Relations API

POST :8084/api/relation

Testing Guide
Step 1: Login

POST :8081/api/login

Request:
{
"email": "hr@xyz.com
",
"password": "pass123"
}

Response:
HR:E001:TOKEN

Step 2: Use Token

Add header:
Authorization: HR:E001:TOKEN

Key Test Scenarios

Hiring Flow:

Valid candidate → AI evaluates → score ≥ 70 → shortlisted
Low score → rejected

Leave Flow:

AI checks leave balance, projects, performance
Returns APPROVE or REJECT with risk score

Auth:

Missing token → error
Wrong role → access denied

The system includes:

Positive test cases
Negative test cases
Edge cases

Internal Flow Explanation

Hiring Flow
Request received at /hiring
Validate input fields
Check duplicate candidate
AI evaluates resume
Decision:
Shortlist → schedule interview + send email
Reject → send rejection email
Store result in database

Leave Flow
Request received at /api/leave
Fetch employee context from DB Layer
AI evaluates request
Decision:
APPROVE or REJECT
Save result and notify user
UI (Concept)

The system can be integrated with a UI containing:

Login page
Candidate application form
HR dashboard
Leave management dashboard
Interview scheduling view

UI interacts with Experience API (Port 8081)

Setup Instructions
Prerequisites
MuleSoft Anypoint Studio
MySQL Database
SMTP configuration
AI API Key
Run Services

8081 → Main API
8082 → Leave API
8083 → DB Layer (internal only)
8084 → Relations API
8086 → Hiring API

Security
Token-based authentication
Role-based access control
Input validation
Internal DB layer isolation

Key Features
Agentic AI decision-making
MuleSoft API-led architecture
Microservices-based design
Automated hiring pipeline
Intelligent leave approvals
Email notifications
Centralized database

Future Enhancements
UI dashboard (React)
Advanced analytics
AI model improvements
