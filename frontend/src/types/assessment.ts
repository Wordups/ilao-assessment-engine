export type CurrentState = "manual" | "semi-automated" | "automated";
export type RiskLevel = "low" | "medium" | "high";
export type AssessmentStatus = "draft" | "in_review" | "complete";

export interface AssessmentSectionItem {
  name: string;
  current_state: CurrentState;
  pain_level: number;
  risk_level: RiskLevel;
  notes: string;
}

export interface AssessmentSection {
  description: string;
  dependencies: string[];
  tools: string[];
  items: AssessmentSectionItem[];
}

export interface AutomationOpportunity {
  workflow_stage: string;
  step_name: string;
  opportunity: string;
  expected_impact: string;
  confidence: "medium" | "high";
}

export interface AssessmentPayload {
  title: string;
  organization_name: string;
  sector: string;
  respondent_name: string;
  respondent_email: string;
  status: AssessmentStatus;
  input_section: AssessmentSection;
  logic_section: AssessmentSection;
  automation_section: AssessmentSection;
  output_section: AssessmentSection;
}

export interface Assessment extends AssessmentPayload {
  id: string;
  owner_id: string;
  executive_summary: string;
  automation_opportunities: AutomationOpportunity[];
  created_at: string;
  updated_at: string;
}
