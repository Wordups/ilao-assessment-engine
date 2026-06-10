import { useEffect, useState } from "react";

import { AssessmentDetails } from "./components/AssessmentDetails";
import { AssessmentWizard } from "./components/AssessmentWizard";
import { AuthGate } from "./components/AuthGate";
import { SummaryPanel } from "./components/SummaryPanel";
import { api, type SessionState } from "./lib/api";
import type { Assessment, AssessmentPayload, AssessmentSection } from "./types/assessment";

function blankSection(): AssessmentSection {
  return {
    description: "",
    dependencies: [],
    tools: [],
    items: [],
  };
}

const initialAssessment: AssessmentPayload = {
  title: "Client Intake Workflow Review",
  organization_name: "Example Organization",
  sector: "Nonprofit Legal Services",
  respondent_name: "Jordan Lee",
  respondent_email: "jordan@example.org",
  status: "draft",
  input_section: blankSection(),
  logic_section: blankSection(),
  automation_section: blankSection(),
  output_section: blankSection(),
};

function saveBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

export default function App() {
  const [session, setSession] = useState<SessionState | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [selectedAssessmentId, setSelectedAssessmentId] = useState<string | null>(null);
  const [editingAssessmentId, setEditingAssessmentId] = useState<string | null>(null);
  const [wizardDraft, setWizardDraft] = useState<AssessmentPayload>(initialAssessment);
  const [message, setMessage] = useState("Connect to start documenting workflows.");

  const loadAssessments = async (nextSession: SessionState) => {
    const items = await api.listAssessments(nextSession);
    setAssessments(items);
    setSelectedAssessmentId((current) => current ?? items[0]?.id ?? null);
  };

  useEffect(() => {
    if (!session) {
      return;
    }

    loadAssessments(session)
      .then(() => setMessage("Assessment workspace ready."))
      .catch(() => setMessage("API connection failed. Verify the backend is running."));
  }, [session]);

  const handleSave = async (payload: AssessmentPayload) => {
    if (!session) {
      return;
    }
    const existing = editingAssessmentId ? assessments.find((item) => item.id === editingAssessmentId) : null;
    const saved = existing
      ? await api.updateAssessment(existing.id, payload, session)
      : await api.createAssessment(payload, session);
    setAssessments((current) => {
      const next = current.filter((item) => item.id !== saved.id);
      return [saved, ...next];
    });
    setSelectedAssessmentId(saved.id);
    setEditingAssessmentId(saved.id);
    setWizardDraft(payload);
    setMessage(existing ? "Assessment updated and re-analyzed." : "Assessment saved and analyzed.");
  };

  const exportJson = async (assessment: Assessment) => {
    if (!session) {
      return;
    }
    const blob = await api.exportAssessment(assessment.id, session);
    saveBlob(blob, `${assessment.title.replace(/\s+/g, "-").toLowerCase()}.json`);
  };

  const downloadPdf = async (assessment: Assessment) => {
    if (!session) {
      return;
    }
    const blob = await api.downloadReport(assessment.id, session);
    saveBlob(blob, `${assessment.title.replace(/\s+/g, "-").toLowerCase()}.pdf`);
  };

  const selectedAssessment = assessments.find((item) => item.id === selectedAssessmentId) ?? null;

  const reviewAssessment = async (assessment: Assessment) => {
    if (!session) {
      return;
    }
    const latest = await api.getAssessment(assessment.id, session);
    setSelectedAssessmentId(latest.id);
    setAssessments((current) => [latest, ...current.filter((item) => item.id !== latest.id)]);
    setMessage(`Loaded ${latest.title} for review.`);
  };

  const loadIntoWizard = (assessment: Assessment) => {
    setSelectedAssessmentId(assessment.id);
    setEditingAssessmentId(assessment.id);
    setWizardDraft({
      title: assessment.title,
      organization_name: assessment.organization_name,
      sector: assessment.sector,
      respondent_name: assessment.respondent_name,
      respondent_email: assessment.respondent_email,
      status: assessment.status,
      input_section: assessment.input_section,
      logic_section: assessment.logic_section,
      automation_section: assessment.automation_section,
      output_section: assessment.output_section,
    });
    setMessage(`Reloaded ${assessment.title} into the wizard.`);
  };

  const startNewAssessment = () => {
    setEditingAssessmentId(null);
    setWizardDraft(initialAssessment);
    setMessage("Started a new assessment draft.");
  };

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">ILAO Assessment Engine</p>
          <h1>Map operational workflows, surface automation opportunities, and export leadership-ready reports.</h1>
          <p className="hero-copy">
            The MVP captures Input, Logic, Automation, and Output findings in a structured assessment flow designed
            for repeatable operational reviews.
          </p>
        </div>
        <div className="hero-stats">
          <div>
            <strong>{assessments.length}</strong>
            <span>Saved Assessments</span>
          </div>
          <div>
            <strong>REST + PDF</strong>
            <span>Delivery Outputs</span>
          </div>
          <div>
            <strong>AI-Ready</strong>
            <span>Future Analysis Layer</span>
          </div>
        </div>
      </section>

      {!session ? <AuthGate onReady={setSession} /> : null}

      {session ? (
        <>
          <section className="status-banner">{message}</section>
          <div className="section-header">
            <h2>Assessment Workspace</h2>
            <button className="ghost-button" onClick={startNewAssessment}>
              New Assessment
            </button>
          </div>
          <AssessmentWizard
            initialValue={wizardDraft}
            editingAssessmentId={editingAssessmentId}
            latestAssessment={selectedAssessment}
            onSubmit={handleSave}
          />
          <AssessmentDetails assessment={selectedAssessment} onReloadIntoWizard={loadIntoWizard} />
          <SummaryPanel
            assessments={assessments}
            selectedAssessmentId={selectedAssessmentId}
            onExportJson={exportJson}
            onDownloadPdf={downloadPdf}
            onSelectAssessment={reviewAssessment}
          />
        </>
      ) : null}
    </main>
  );
}
