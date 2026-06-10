import type { Assessment, AssessmentSection } from "../types/assessment";

interface AssessmentDetailsProps {
  assessment: Assessment | null;
  onReloadIntoWizard: (assessment: Assessment) => void;
}

function DetailList({ title, values }: { title: string; values: string[] }) {
  if (!values.length) {
    return null;
  }

  return (
    <div>
      <strong>{title}</strong>
      <p>{values.join(", ")}</p>
    </div>
  );
}

export function AssessmentDetails({ assessment, onReloadIntoWizard }: AssessmentDetailsProps) {
  if (!assessment) {
    return (
      <section className="detail-panel">
        <h2>Assessment Review</h2>
        <p>Select a saved assessment to review its ILAO sections, summary, and generated opportunities.</p>
      </section>
    );
  }

  const sections: Array<{ label: string; section: AssessmentSection }> = [
    { label: "Input", section: assessment.input_section },
    { label: "Logic", section: assessment.logic_section },
    { label: "Automation", section: assessment.automation_section },
    { label: "Output", section: assessment.output_section },
  ];

  return (
    <section className="detail-panel">
      <div className="section-header">
        <h2>{assessment.title}</h2>
        <button className="primary-button" onClick={() => onReloadIntoWizard(assessment)}>
          Load Into Wizard
        </button>
      </div>
      <p className="detail-meta">
        {assessment.organization_name} | {assessment.sector} | Updated {new Date(assessment.updated_at).toLocaleString()}
      </p>
      <article className="summary-card">
        <h3>Executive Summary</h3>
        <p>{assessment.executive_summary}</p>
      </article>
      <article className="summary-card">
        <h3>Automation Opportunities</h3>
        <ul>
          {assessment.automation_opportunities.map((item) => (
            <li key={`${assessment.id}-${item.workflow_stage}-${item.step_name}`}>
              <strong>{item.workflow_stage}:</strong> {item.opportunity}
            </li>
          ))}
        </ul>
      </article>
      <div className="detail-grid">
        {sections.map(({ label, section }) => (
          <article className="summary-card" key={label}>
            <h3>{label}</h3>
            <p>{section.description || "No description provided."}</p>
            <DetailList title="Dependencies" values={section.dependencies} />
            <DetailList title="Tools" values={section.tools} />
            <ul>
              {section.items.map((item) => (
                <li key={`${label}-${item.name}`}>
                  <strong>{item.name}</strong> | {item.current_state} | pain {item.pain_level}/5 | risk {item.risk_level}
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}
