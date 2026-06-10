import type { Assessment } from "../types/assessment";

interface SummaryPanelProps {
  assessments: Assessment[];
  selectedAssessmentId?: string | null;
  onExportJson: (assessment: Assessment) => Promise<void>;
  onDownloadPdf: (assessment: Assessment) => Promise<void>;
  onSelectAssessment: (assessment: Assessment) => void;
}

export function SummaryPanel({ assessments, selectedAssessmentId, onExportJson, onDownloadPdf, onSelectAssessment }: SummaryPanelProps) {
  return (
    <section className="summary-layout">
      <div className="section-header">
        <h2>Recent Assessments</h2>
      </div>
      <div className="assessment-grid">
        {assessments.map((assessment) => (
          <article className={`assessment-card ${selectedAssessmentId === assessment.id ? "selected" : ""}`} key={assessment.id}>
            <div className="card-topline">
              <span>{assessment.organization_name}</span>
              <span className="status-chip">{assessment.status.replace("_", " ")}</span>
            </div>
            <h3>{assessment.title}</h3>
            <p>{assessment.executive_summary}</p>
            <div className="opportunity-list">
              {assessment.automation_opportunities.slice(0, 3).map((item) => (
                <div className="opportunity-chip" key={`${assessment.id}-${item.step_name}`}>
                  {item.workflow_stage}: {item.step_name}
                </div>
              ))}
            </div>
            <div className="card-actions">
              <button className="ghost-button" onClick={() => onSelectAssessment(assessment)}>
                Review
              </button>
              <button className="ghost-button" onClick={() => onExportJson(assessment)}>
                Export JSON
              </button>
              <button className="primary-button" onClick={() => onDownloadPdf(assessment)}>
                PDF Report
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
