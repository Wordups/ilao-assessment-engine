CREATE TABLE assessments (
    id UUID PRIMARY KEY,
    owner_id VARCHAR(128) NOT NULL,
    title VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) NOT NULL,
    sector VARCHAR(120) NOT NULL,
    respondent_name VARCHAR(255) NOT NULL,
    respondent_email VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    input_section JSONB NOT NULL,
    logic_section JSONB NOT NULL,
    automation_section JSONB NOT NULL,
    output_section JSONB NOT NULL,
    executive_summary TEXT NOT NULL,
    automation_opportunities JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_assessments_owner_id ON assessments(owner_id);
CREATE INDEX idx_assessments_organization_name ON assessments(organization_name);
