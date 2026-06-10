import { useEffect, useState } from "react";

import type { Assessment, AssessmentPayload, AssessmentSection, AssessmentSectionItem, CurrentState, RiskLevel } from "../types/assessment";

const stages: Array<keyof Pick<AssessmentPayload, "input_section" | "logic_section" | "automation_section" | "output_section">> = [
  "input_section",
  "logic_section",
  "automation_section",
  "output_section",
];

const sectionLabels: Record<(typeof stages)[number], string> = {
  input_section: "Input",
  logic_section: "Logic",
  automation_section: "Automation",
  output_section: "Output",
};

interface WizardProps {
  initialValue: AssessmentPayload;
  editingAssessmentId?: string | null;
  latestAssessment?: Assessment | null;
  onSubmit: (payload: AssessmentPayload) => Promise<void>;
}

function updateList(value: string): string[] {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

function createItem(): AssessmentSectionItem {
  return {
    name: "",
    current_state: "manual",
    pain_level: 3,
    risk_level: "medium",
    notes: "",
  };
}

export function AssessmentWizard({ initialValue, editingAssessmentId, latestAssessment, onSubmit }: WizardProps) {
  const [form, setForm] = useState<AssessmentPayload>(initialValue);
  const [step, setStep] = useState(0);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm(initialValue);
    setStep(0);
  }, [initialValue, editingAssessmentId]);

  const sectionKey = stages[Math.max(0, step - 1)];

  const updateSection = (key: keyof AssessmentPayload, value: AssessmentSection) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const currentSection = sectionKey ? form[sectionKey] : null;

  const submit = async () => {
    setSaving(true);
    try {
      await onSubmit(form);
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="wizard-shell">
      <div className="wizard-steps">
        {["Profile", "Input", "Logic", "Automation", "Output", "Review"].map((label, index) => (
          <button
            key={label}
            className={`step-pill ${index === step ? "active" : ""}`}
            onClick={() => setStep(index)}
            type="button"
          >
            {label}
          </button>
        ))}
      </div>

      {step === 0 ? (
        <div className="panel-grid">
          <label>
            Assessment Title
            <input value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} />
          </label>
          <label>
            Organization Name
            <input
              value={form.organization_name}
              onChange={(event) => setForm({ ...form, organization_name: event.target.value })}
            />
          </label>
          <label>
            Sector
            <input value={form.sector} onChange={(event) => setForm({ ...form, sector: event.target.value })} />
          </label>
          <label>
            Respondent Name
            <input
              value={form.respondent_name}
              onChange={(event) => setForm({ ...form, respondent_name: event.target.value })}
            />
          </label>
          <label>
            Respondent Email
            <input
              type="email"
              value={form.respondent_email}
              onChange={(event) => setForm({ ...form, respondent_email: event.target.value })}
            />
          </label>
          <label>
            Status
            <select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value as Assessment["status"] })}>
              <option value="draft">Draft</option>
              <option value="in_review">In Review</option>
              <option value="complete">Complete</option>
            </select>
          </label>
        </div>
      ) : null}

      {currentSection ? (
        <div className="section-editor">
          <div className="section-header">
            <h2>{sectionLabels[sectionKey]}</h2>
            <button
              type="button"
              className="ghost-button"
              onClick={() =>
                updateSection(sectionKey, {
                  ...currentSection,
                  items: [...currentSection.items, createItem()],
                })
              }
            >
              Add Step
            </button>
          </div>
          <label>
            Description
            <textarea
              rows={4}
              value={currentSection.description}
              onChange={(event) =>
                updateSection(sectionKey, {
                  ...currentSection,
                  description: event.target.value,
                })
              }
            />
          </label>
          <div className="panel-grid">
            <label>
              Dependencies
              <textarea
                rows={4}
                value={currentSection.dependencies.join("\n")}
                onChange={(event) =>
                  updateSection(sectionKey, {
                    ...currentSection,
                    dependencies: updateList(event.target.value),
                  })
                }
              />
            </label>
            <label>
              Tools
              <textarea
                rows={4}
                value={currentSection.tools.join("\n")}
                onChange={(event) =>
                  updateSection(sectionKey, {
                    ...currentSection,
                    tools: updateList(event.target.value),
                  })
                }
              />
            </label>
          </div>
          <div className="item-stack">
            {currentSection.items.map((item, index) => (
              <div className="item-card" key={`${item.name}-${index}`}>
                <div className="item-grid">
                  <label>
                    Step Name
                    <input
                      value={item.name}
                      onChange={(event) => {
                        const next = [...currentSection.items];
                        next[index] = { ...item, name: event.target.value };
                        updateSection(sectionKey, { ...currentSection, items: next });
                      }}
                    />
                  </label>
                  <label>
                    Current State
                    <select
                      value={item.current_state}
                      onChange={(event) => {
                        const next = [...currentSection.items];
                        next[index] = { ...item, current_state: event.target.value as CurrentState };
                        updateSection(sectionKey, { ...currentSection, items: next });
                      }}
                    >
                      <option value="manual">Manual</option>
                      <option value="semi-automated">Semi-Automated</option>
                      <option value="automated">Automated</option>
                    </select>
                  </label>
                  <label>
                    Pain Level
                    <input
                      type="range"
                      min={1}
                      max={5}
                      value={item.pain_level}
                      onChange={(event) => {
                        const next = [...currentSection.items];
                        next[index] = { ...item, pain_level: Number(event.target.value) };
                        updateSection(sectionKey, { ...currentSection, items: next });
                      }}
                    />
                  </label>
                  <label>
                    Risk Level
                    <select
                      value={item.risk_level}
                      onChange={(event) => {
                        const next = [...currentSection.items];
                        next[index] = { ...item, risk_level: event.target.value as RiskLevel };
                        updateSection(sectionKey, { ...currentSection, items: next });
                      }}
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </label>
                </div>
                <label>
                  Notes
                  <textarea
                    rows={3}
                    value={item.notes}
                    onChange={(event) => {
                      const next = [...currentSection.items];
                      next[index] = { ...item, notes: event.target.value };
                      updateSection(sectionKey, { ...currentSection, items: next });
                    }}
                  />
                </label>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {step === 5 ? (
        <div className="review-grid">
          <article className="summary-card">
            <h2>{editingAssessmentId ? "Ready to Update" : "Ready to Save"}</h2>
            <p>
              This submission will {editingAssessmentId ? "update" : "store"} the assessment, generate an executive
              summary, and produce automation opportunities.
            </p>
            <button className="primary-button" disabled={saving} onClick={submit}>
              {saving ? "Saving..." : editingAssessmentId ? "Update Assessment" : "Save Assessment"}
            </button>
          </article>
          <article className="summary-card">
            <h2>Latest Analysis</h2>
            {latestAssessment ? (
              <>
                <p>{latestAssessment.executive_summary}</p>
                <ul>
                  {latestAssessment.automation_opportunities.slice(0, 4).map((item) => (
                    <li key={`${item.workflow_stage}-${item.step_name}`}>{item.workflow_stage}: {item.opportunity}</li>
                  ))}
                </ul>
              </>
            ) : (
              <p>Save an assessment to view generated analysis.</p>
            )}
          </article>
        </div>
      ) : null}

      <div className="wizard-actions">
        <button type="button" className="ghost-button" disabled={step === 0} onClick={() => setStep((current) => current - 1)}>
          Back
        </button>
        <button type="button" className="primary-button" disabled={step === 5} onClick={() => setStep((current) => current + 1)}>
          Next
        </button>
      </div>
    </section>
  );
}
