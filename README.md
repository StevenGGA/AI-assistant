# AI Workflow Assistant for Student Projects

An intelligent project management system with OAuth-based integrations for Google Drive, Slack, and Canvas LMS.

## Features
- AI-powered task extraction and meeting summarization
- OAuth authentication for all integrations (no API keys needed!)
- Canvas LMS integration for assignment sync
- Slack integration for team communication
- Google Drive for document management
- Automated weekly progress reports

## Quick Start

1. Clone the repository
2. Run the setup script: `./setup.sh`
3. Configure OAuth: `./setup-oauth.sh`
4. Start the application: `docker-compose up -d`
5. Access at http://localhost:3000

## Documentation

See `/docs/OAUTH_SETUP.md` for OAuth configuration guide.

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: React
- Database: PostgreSQL
- AI: Qwen2.5-3B-Instruct
- Container: Docker

## License
MIT
