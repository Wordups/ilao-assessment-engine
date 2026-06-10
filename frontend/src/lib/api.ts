import type { Assessment, AssessmentPayload } from "../types/assessment";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export interface SessionState {
  token?: string;
  devUserId?: string;
}

async function request<T>(path: string, options: RequestInit = {}, session?: SessionState): Promise<T> {
  const headers = new Headers(options.headers ?? {});
  headers.set("Content-Type", "application/json");
  if (session?.token) {
    headers.set("Authorization", `Bearer ${session.token}`);
  } else if (session?.devUserId) {
    headers.set("X-Dev-User", session.devUserId);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  getCurrentUser: (session?: SessionState) => request<{ user_id: string; email?: string; auth_mode: string }>("/auth/me", {}, session),
  listAssessments: (session?: SessionState) => request<Assessment[]>("/assessments", {}, session),
  getAssessment: (id: string, session?: SessionState) => request<Assessment>(`/assessments/${id}`, {}, session),
  createAssessment: (payload: AssessmentPayload, session?: SessionState) =>
    request<Assessment>("/assessments", { method: "POST", body: JSON.stringify(payload) }, session),
  updateAssessment: (id: string, payload: AssessmentPayload, session?: SessionState) =>
    request<Assessment>(`/assessments/${id}`, { method: "PUT", body: JSON.stringify(payload) }, session),
  exportAssessment: async (id: string, session?: SessionState) => {
    const headers = new Headers();
    if (session?.token) {
      headers.set("Authorization", `Bearer ${session.token}`);
    } else if (session?.devUserId) {
      headers.set("X-Dev-User", session.devUserId);
    }
    const response = await fetch(`${API_BASE_URL}/assessments/${id}/export`, { headers });
    if (!response.ok) {
      throw new Error("Failed to export assessment.");
    }
    return response.blob();
  },
  downloadReport: async (id: string, session?: SessionState) => {
    const headers = new Headers();
    if (session?.token) {
      headers.set("Authorization", `Bearer ${session.token}`);
    } else if (session?.devUserId) {
      headers.set("X-Dev-User", session.devUserId);
    }
    const response = await fetch(`${API_BASE_URL}/assessments/${id}/report`, { headers });
    if (!response.ok) {
      throw new Error("Failed to generate report.");
    }
    return response.blob();
  },
};
