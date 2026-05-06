# 🚀 AI Log Analyzer

> An AI-powered log analysis API that automatically detects errors, summarizes issues, and suggests fixes — deployed with a full CI/CD pipeline on AWS.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![AWS EC2](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions)
![Groq AI](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)

---

## 🌐 Live API

```
http://3.110.148.208
```

---

## 📌 Table of Contents

- [What It Does](#-what-it-does)
- [Tech Stack](#-tech-stack)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [How to Run Locally](#-how-to-run-locally)
- [Environment Variables](#-environment-variables)
- [How Deployment Works](#-how-deployment-works)

---

## 💡 What It Does

Paste any server log into the API and get back an instant AI-generated analysis:

- 🔍 **Summary** — What is happening in the logs
- ⚠️ **Errors** — What went wrong and why
- 💡 **Suggestions** — How to fix it

Powered by **Groq's LLaMA 3.3 70B** model for fast, accurate DevOps insights.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11 |
| **Framework** | Flask |
| **AI Model** | Groq — LLaMA 3.3 70B |
| **Containerization** | Docker |
| **Cloud Server** | AWS EC2 (Ubuntu 22.04) |
| **Image Registry** | AWS ECR |
| **CI/CD** | GitHub Actions |
| **CORS** | Flask-CORS |

---

## ⚙️ CI/CD Pipeline

Every time code is pushed to the `main` branch, the following happens **automatically**:

```
Developer pushes code
        │
        ▼
┌─────────────────────┐
│    GitHub Actions   │
│                     │
│  1. Checkout code   │
│  2. Login to AWS    │
│  3. Build Docker    │
│     image           │
│  4. Push image      │
│     to AWS ECR      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│    AWS EC2 Server   │
│                     │
│  5. Pull new image  │
│     from ECR        │
│  6. Stop old        │
│     container       │
│  7. Start new       │
│     container       │
└─────────────────────┘
         │
         ▼
  🌐 App is live at
  http://3.110.148.208
```

### Pipeline Workflow File

Located at `.github/workflows/deploy.yml`

**Job 1 — Build & Push:**
- Logs into AWS using GitHub Secrets
- Builds the Docker image
- Pushes it to Amazon ECR with two tags: `latest` and the commit SHA

**Job 2 — Deploy (runs only if Job 1 passes):**
- SSHs into the EC2 server
- Pulls the latest Docker image from ECR
- Stops and removes the old container
- Starts a new container with the updated image

---

## 📁 Project Structure

```
DevOps_aws/
│
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD pipeline definition
│
├── app.py                    # Main Flask application
├── Dockerfile                # Docker build instructions
├── .dockerignore             # Files excluded from Docker image
└── README.md                 # This file
```

---

## 📡 API Endpoints

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{
  "status": "running",
  "message": "🚀 AI Log Analyzer API is live"
}
```

---

### `POST /analyze`
Analyzes logs using AI and returns a structured report.

**Request:**
```json
{
  "logs": "ERROR: Connection refused on port 5432"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": "🔍 Summary: ...\n⚠️ Errors: ...\n💡 Suggestions: ..."
}
```

**Test it with curl:**
```bash
curl -X POST http://3.110.148.208/analyze \
  -H "Content-Type: application/json" \
  -d '{"logs": "ERROR: Connection refused on port 5432"}'
```

---

## 💻 How to Run Locally

### Prerequisites
- Python 3.11+
- Docker (optional for local container test)

### 1. Clone the repository
```bash
git clone https://github.com/kashish1326/DevOps_aws.git
cd DevOps_aws
```

### 2. Create a `.env` file
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install dependencies
```bash
pip install flask python-dotenv groq flask-cors
```

### 4. Run the app
```bash
python app.py
```

App will be live at `http://localhost:5000`

### Run with Docker locally
```bash
docker build -t ai-log-analyzer .
docker run -p 5000:5000 -e GROQ_API_KEY=your_key ai-log-analyzer
```

---

## 🔐 Environment Variables

| Variable | Description | Where to Set |
|----------|-------------|--------------|
| `GROQ_API_KEY` | Groq API key for AI model | GitHub Secrets + `.env` locally |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key | GitHub Secrets |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key | GitHub Secrets |
| `AWS_REGION` | AWS region (e.g. ap-south-1) | GitHub Secrets |
| `ECR_REPOSITORY` | ECR repository name | GitHub Secrets |
| `EC2_HOST` | EC2 public IP address | GitHub Secrets |
| `EC2_USERNAME` | EC2 login user (ubuntu) | GitHub Secrets |
| `EC2_PRIVATE_KEY` | Contents of .pem key file | GitHub Secrets |

---

## 🚀 How Deployment Works

### Infrastructure

```
┌─────────────────────────────────────────────┐
│                  AWS Cloud                  │
│                                             │
│   ┌─────────────┐      ┌────────────────┐   │
│   │  Amazon ECR │      │   Amazon EC2   │   │
│   │             │ pull │                │   │
│   │ Docker image│─────▶│ Docker container│  │
│   │  repository │      │  (Flask app)   │   │
│   └─────────────┘      └────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### GitHub Secrets Required

All sensitive values are stored as **GitHub Actions Secrets** — never hardcoded in the code. This keeps API keys and credentials secure.

### Docker Container

The app runs inside a Docker container on EC2:
- Port `5000` inside the container
- Mapped to port `80` publicly
- Configured to auto-restart if the server reboots (`--restart always`)

---

## 👤 Author

**Kashish**
GitHub: [@kashish1326](https://github.com/kashish1326)

---

*Built as part of an entrepreneurship and AI agents project — demonstrating real-world DevOps practices with CI/CD, containerization, and cloud deployment.*
