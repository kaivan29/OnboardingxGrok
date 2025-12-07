import { api } from "@/lib/api-client";

// Types
export interface UploadResponse {
  id: string;
  fileName: string;
  status: "pending" | "processing" | "completed" | "failed";
  message?: string;
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
   * @returns Upload response with file ID and status
   */
  uploadResume: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("resume", file);

    // TODO: Replace with actual API endpoint
    // const response = await api.post<UploadResponse>("/onboarding/upload", formData, {
    const response = await api.post<UploadResponse>("/analyzeResume", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;

    // Placeholder: Simulate API response
    console.log("📤 Uploading resume:", file.name);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    return {
      id: `upload_${Date.now()}`,
      fileName: file.name,
      status: "processing",
      message: "Resume uploaded successfully",
    };
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
