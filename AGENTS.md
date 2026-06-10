# AGENTS.md

## Mission

Future contributors should preserve the ILAO workflow focus of this application:

- Input
- Logic
- Automation
- Output

Every change should improve one of these outcomes: assessment capture quality, analysis quality, reporting quality, or platform extensibility.

## Working Agreements

- Respect clean architecture boundaries.
- Keep business rules in `backend/app/domain`.
- Keep orchestration in `backend/app/application`.
- Keep FastAPI route concerns in `backend/app/presentation`.
- Keep persistence, external integrations, and deployment wiring in `backend/app/infrastructure`.
- Prefer additive changes over broad rewrites.
- Do not break JSON export or PDF generation contracts without updating docs and sample data.

## Frontend Conventions

- Preserve the multi-step wizard UX.
- Keep components focused and typed with shared models from `frontend/src/types`.
- Favor responsive layouts and clear assessment language over generic dashboard patterns.
- Treat Supabase as the authentication source of truth when configured.

## Backend Conventions

- Add new analysis capabilities behind ports and services so future AI features remain swappable.
- Keep API routes thin.
- Validate all request and response models with Pydantic schemas.
- Add or update tests for domain logic when behavior changes.

## Documentation Checklist

Update these artifacts when relevant:

- `README.md`
- `docs/architecture.md`
- `docs/database-schema.md`
- `docs/api.md`
- `sample-data/sample_assessment.json`

## Suggested Next Enhancements

- Add migration tooling with Alembic
- Add organization and team membership models
- Add versioned assessment templates
- Add AI-assisted scoring and benchmark comparisons
