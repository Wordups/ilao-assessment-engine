# ILAO Assessment Engine

ILAO Assessment Engine is an open workflow discovery tool that helps teams document how work enters, moves through, and exits an organization, then identify ownership gaps, bottlenecks, automation opportunities, and measurable outputs.

Repository: [Wordups/ilao-assessment-engine](https://github.com/Wordups/ilao-assessment-engine)

This project applies the ILAO framework:

- `Input`: how work enters the system
- `Logic`: how decisions, rules, and approvals shape the flow
- `Automation`: where tools, integrations, and repeatable actions reduce manual effort
- `Output`: what leaves the system and how it is measured

## What The Assessment Engine Does

The MVP provides:

- a multi-step React assessment wizard
- a FastAPI backend with a REST API
- PostgreSQL-backed persistence for saved assessments
- executive summary generation from assessment responses
- automation opportunity generation from documented workflow friction
- JSON export and PDF report export
- a review flow for reloading prior assessments into the wizard
- a public-facing static landing page for GitHub Pages

## Tech Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL
- Authentication: Supabase Auth integration points with local development fallback
- Testing: Pytest + Playwright
- Deployment: Docker Compose locally, GitHub Actions for CI, GitHub Pages for the public project site

## Project Structure

```text
ilao-assessment-engine/
  backend/
  frontend/
  docs/
  docs-site/
  sample-data/
  .github/workflows/
```

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Backend docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend will be available at [http://localhost:5173](http://localhost:5173).

### Optional UI Smoke Test

```bash
cd frontend
npx playwright install chromium
npm run test:e2e
```

## Docker Setup

Run the full stack with Docker Compose:

```bash
docker compose up --build
```

Default ports:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)
- PostgreSQL: `localhost:5432`

## API Overview

Base path: `/api/v1`

- `GET /auth/me`: returns the active user identity and auth mode
- `GET /assessments`: lists assessments for the active user
- `POST /assessments`: creates an assessment and generates analysis outputs
- `GET /assessments/{assessment_id}`: returns one assessment
- `PUT /assessments/{assessment_id}`: updates an assessment and regenerates outputs
- `GET /assessments/{assessment_id}/export`: downloads assessment JSON
- `GET /assessments/{assessment_id}/report`: downloads the PDF report

Additional API notes live in [docs/api.md](docs/api.md).

## Screenshots

Add screenshots here before publishing the repository landing page:

- `docs/screenshots/wizard-overview.png`
- `docs/screenshots/assessment-review.png`
- `docs/screenshots/pdf-report.png`

Suggested captions:

- workflow capture wizard
- saved assessment review view
- executive-ready PDF output

## GitHub Pages

The repository includes a public static site in `docs-site/` that explains the ILAO framework and the project.

Deployment notes: [docs/deployment-github-pages.md](docs/deployment-github-pages.md).

Before publishing:

1. Update the placeholder GitHub repository link in `docs-site/index.html`.
2. Enable GitHub Pages with `GitHub Actions` as the source.
3. Push the repository to `main` or `master`.

## Roadmap

- configurable assessment templates for different operating models
- richer scoring and benchmark comparisons
- cross-assessment dashboards and reporting history
- organization branding controls for exported reports
- optional AI-assisted analysis providers layered onto the current clean architecture

## Portfolio / Case Study Positioning

This repository is suitable as a portfolio project or case study because it demonstrates:

- workflow discovery and operational systems thinking
- end-to-end product design across frontend, backend, persistence, and exports
- clean architecture boundaries for future extension
- public documentation, CI setup, and deployment readiness
- a practical path from process mapping to automation planning

## Public Repository Notes

- No secrets or API keys are included.
- Environment values should be copied from the provided example files.
- Sample data uses placeholder organizations and non-sensitive examples.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
