import { api } from "@/lib/api-client";

// Types
export interface UploadResponse {
  success: boolean;
  profile_id: string;
  message: string;
  is_duplicate: boolean;
  analysis: {
    candidate_name: string;
    experience_years: number;
    education: any[];
    technical_skills: {
      languages: string[];
      frameworks: string[];
      tools: string[];
      databases: string[];
    };
    experience_summary: any[];
    strengths: string[];
    knowledge_gaps: string[];
    recommended_learning_path: string[];
  };
  study_plan?: {
    success: boolean;
    profile_id: string;
    repo_url: string;
    plan_id: string;
    duration_weeks: number;
    plan: {
      weeks: any[];
    };
  };
}

export interface ProcessingStatus {
  id: string;
  currentStep: number;
  totalSteps: number;
  stepName: string;
  status: "pending" | "processing" | "completed" | "failed";
  result?: {
    tutorialId?: string;
    dashboardUrl?: string;
  };
}

// API endpoints for onboarding
export const onboardingApi = {
  /**
   * Upload resume file
   * @param file - The resume file to upload
   * @returns Upload response with profile analysis and study plan
   */
  uploadResume: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("repo_url", "https://github.com/facebook/rocksdb");
    formData.append("generate_plan", "true");

    const response = await api.post<UploadResponse>("/analyzeResume", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },

  /**
   * Get processing status for uploaded resume
   * @param uploadId - The upload ID to check status for
   * @returns Current processing status
   */
  getProcessingStatus: async (uploadId: string): Promise<ProcessingStatus> => {
    // TODO: Replace with actual API endpoint
    // const response = await api.get<ProcessingStatus>(`/api/onboarding/status/${uploadId}`);
    // return response.data;

    // Placeholder: Simulate API response
    console.log("📊 Checking status for:", uploadId);
    return {
      id: uploadId,
      currentStep: 0,
      totalSteps: 6,
      stepName: "Initializing",
      status: "processing",
    };
  }
};
