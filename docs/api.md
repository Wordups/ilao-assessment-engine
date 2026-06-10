# API Documentation

Base URL: `http://localhost:8000/api/v1`

Interactive OpenAPI docs are available at `http://localhost:8000/docs`.

## Authentication

- Development mode: send `X-Dev-User: dev-user`
- Supabase mode: send `Authorization: Bearer <access_token>`

## Endpoints

### `GET /auth/me`

Returns the active user identity and auth mode.

### `GET /assessments`

Returns all assessments for the authenticated user.

### `POST /assessments`

Creates an assessment and generates:

- executive summary
- automation opportunities

Request body matches the sample payload in `sample-data/sample_assessment.json`.

### `GET /assessments/{assessment_id}`

Returns a single assessment.

### `PUT /assessments/{assessment_id}`

Updates an assessment and regenerates analysis outputs.

### `GET /assessments/{assessment_id}/export`

Downloads the assessment as formatted JSON.

### `GET /assessments/{assessment_id}/report`

Downloads an executive-style PDF report with summary scorecards and workflow section tables.
