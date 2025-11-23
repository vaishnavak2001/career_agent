# Architecture Overview

## High-Level Architecture

The Career Agent is a modular, event-driven system designed to automate the job application process. It consists of the following core components:

1.  **Frontend (React + Tailwind)**: A responsive web interface for users to manage their profile, view job matches, and track applications. It communicates with the backend via REST API.
2.  **Backend (FastAPI)**: The core application logic, exposing APIs for the frontend and handling background tasks.
3.  **Agent Orchestrator (LangChain)**: An intelligent agent that coordinates various tools (scraping, parsing, matching, applying) to achieve the user's goals.
4.  **Database (PostgreSQL)**: Stores all persistent data, including user profiles, resumes, jobs, applications, and analytics.
5.  **Browser Automation (Playwright)**: Handles interaction with job boards for scraping and auto-applying.
6.  **External Integrations**: Connects to third-party services like OpenAI (LLM), SendGrid (Email), and various job boards.

## Component Diagram

```mermaid
graph TD
    User[User] -->|HTTPS| Frontend[React Frontend]
    Frontend -->|REST API| Backend[FastAPI Backend]
    
    subgraph Backend Services
        Backend -->|Orchestrates| Agent[LangChain Agent]
        Agent -->|Calls| Tools[Tools Layer]
        Tools -->|Scrapes| Scraper[Playwright Scraper]
        Tools -->|Parses| Parser[Resume/JD Parser]
        Tools -->|Scores| Matcher[Match Scorer]
        Tools -->|Generates| Generator[Cover Letter Gen]
    end
    
    subgraph Data Layer
        Backend -->|Reads/Writes| DB[(PostgreSQL)]
        Backend -->|Stores Files| Storage[S3/Local Storage]
    end
    
    subgraph External World
        Scraper -->|HTTP/Browser| JobBoards[Indeed, LinkedIn, etc.]
        Agent -->|API| LLM[LLM Provider (OpenAI)]
        Backend -->|SMTP/API| Email[Email Service]
    end
```

## Data Flow

1.  **Job Discovery**: The Scheduler triggers the Scraper to fetch new jobs from configured sources.
2.  **Processing**:
    *   **Deduplication**: Jobs are checked against the database to avoid duplicates.
    *   **Scam Detection**: Jobs are analyzed for scam indicators.
    *   **Parsing**: Job descriptions are parsed into structured data.
3.  **Matching**: The Matcher compares the job against the user's resume and profile to calculate a Match Score.
4.  **Action**:
    *   If the score exceeds the threshold, the Agent initiates the application process.
    *   **Project Search**: Relevant projects are found and added to the resume.
    *   **Resume Tailoring**: The resume is rewritten to highlight relevant skills.
    *   **Cover Letter**: A personalized cover letter is generated.
5.  **Application**: The Auto-Applier submits the application (if enabled) or queues it for user review.
6.  **Feedback**: Application status is tracked, and analytics are updated.

## Tech Stack

*   **Frontend**: React, Vite, Tailwind CSS
*   **Backend**: Python, FastAPI
*   **Database**: PostgreSQL, SQLAlchemy
*   **AI/ML**: LangChain, OpenAI GPT-4/3.5
*   **Automation**: Playwright
*   **Infrastructure**: Docker, GitHub Actions, Render/Railway/Vercel
