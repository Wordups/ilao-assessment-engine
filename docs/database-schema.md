# Database Schema

## Table: `assessments`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID | Primary key |
| `owner_id` | varchar(128) | Supabase user id or development user id |
| `title` | varchar(255) | Assessment title |
| `organization_name` | varchar(255) | Organization being assessed |
| `sector` | varchar(120) | Industry or sector |
| `respondent_name` | varchar(255) | Assessment respondent |
| `respondent_email` | varchar(255) | Respondent email |
| `status` | varchar(50) | `draft`, `in_review`, `complete` |
| `input_section` | JSONB | Input stage content |
| `logic_section` | JSONB | Logic stage content |
| `automation_section` | JSONB | Automation stage content |
| `output_section` | JSONB | Output stage content |
| `executive_summary` | text | Generated narrative summary |
| `automation_opportunities` | JSONB | Generated opportunity list |
| `created_at` | timestamptz | Created timestamp |
| `updated_at` | timestamptz | Updated timestamp |

## SQL Reference

See [schema.sql](/C:/Users/bword/OneDrive/Documents/New%20project/ilao-assessment-engine/docs/schema.sql).
