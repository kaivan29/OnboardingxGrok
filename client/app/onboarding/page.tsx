"use client";
import React, { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { FileUpload } from "@/components/ui/file-upload";
import { MultiStepLoader } from "@/components/ui/multi-step-loader";
import { IconSquareRoundedX } from "@tabler/icons-react";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, AlertCircle } from "lucide-react";
import { onboardingApi } from "@/lib/api/onboarding";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const loadingStates = [
  { text: "Uploading resume..." },
  { text: "Analyzing your experience with AI" },
  { text: "Identifying technical skills and gaps" },
  { text: "Analyzing codebase structure" },
  { text: "Generating personalized learning path" },
  { text: "Creating weekly tasks and chapters" },
  { text: "Finalizing your custom study plan" },
];

interface AnalysisResult {
  profile_id: string;
  is_duplicate: boolean;
  analysis: {
    candidate_name: string;
    experience_years: number;
    technical_skills: {
      languages: string[];
      frameworks: string[];
      tools: string[];
      databases: string[];
    };
    knowledge_gaps: string[];
    strengths: string[];
  };
  study_plan?: {
    plan_id: string;
    duration_weeks: number;
    plan: {
      weeks: any[];
    };
  };
}

export default function OnboardingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleFileUpload = useCallback(async (uploadedFiles: File[]) => {
    if (uploadedFiles.length === 0) return;

    setFiles(uploadedFiles);
    setLoading(true);
    setShowConfirmation(false);

    try {
      // Upload the resume - backend will automatically:
      // 1. Detect duplicates using file hash
      // 2. Analyze resume with Grok
      // 3. Generate personalized study plan
      const result = await onboardingApi.uploadResume(uploadedFiles[0]);
      console.log("Analysis complete:", result);

      // Store the complete result
      setAnalysisResult(result);

      // Show success message
      if (result.is_duplicate) {
        toast.success("Resume already analyzed! Using existing profile.");
      } else {
        toast.success("Resume analyzed successfully!");
      }

      // Show confirmation dialog after a short delay
      setTimeout(() => {
        setLoading(false);
        setShowConfirmation(true);
      }, 1500);

    } catch (err: any) {
      console.error("Upload failed:", err);
      const errorMsg = err.response?.data?.detail || "Failed to analyze resume. Please try again.";
      toast.error(errorMsg);
      setLoading(false);
      setShowConfirmation(false);
    }
  }, []);

  const handleConfirm = useCallback(() => {
    // Store profile_id in localStorage for later use
    if (analysisResult) {
      localStorage.setItem('profile_id', analysisResult.profile_id);
      if (analysisResult.study_plan) {
        localStorage.setItem('plan_id', analysisResult.study_plan.plan_id);
      }
    }

    toast.success("Let's start your personalized onboarding!");
    router.push("/dashboard");
  }, [analysisResult, router]);

  const handleClose = useCallback(() => {
    setLoading(false);
  }, []);

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="flex h-14 w-full items-center justify-between border-b border-gray-200 px-6 lg:px-12 bg-white">
        <Link href="/" className="flex items-center gap-3 group">
          <ArrowLeft className="w-4 h-4 text-gray-600 group-hover:text-black transition-colors" />
          <div className="flex items-center gap-3">
            <div className="grid grid-cols-3 gap-1 w-6 h-6">
              {[...Array(9)].map((_, i) => (
                <div
                  key={i}
                  className={`w-1 h-1 rounded-full ${i % 2 === 0 ? "bg-black" : "bg-gray-400"}`}
                />
              ))}
            </div>
            <span className="text-xl font-semibold tracking-tight text-black">
              Grokboard
            </span>
          </div>
        </Link>
      </header>

      {/* Main Content */}
      <div className="flex flex-col items-center justify-center px-6 py-16 lg:py-24">
        {!showConfirmation ? (
          <>
            <div className="max-w-2xl w-full text-center mb-12">
              <h1 className="text-4xl lg:text-5xl font-medium tracking-tight text-black mb-4">
                Upload Your Resume
              </h1>
              <p className="text-lg text-gray-600 leading-relaxed">
                We'll analyze your experience with AI and generate a personalized
                study plan tailored to your background and knowledge gaps.
              </p>
            </div>

            {/* File Upload */}
            <div className="w-full max-w-2xl border border-dashed border-gray-200 rounded-lg bg-gray-50/50">
              <FileUpload onChange={handleFileUpload} />
            </div>

            {files.length > 0 && !loading && (
              <p className="mt-4 text-sm text-gray-500">
                {files.length} file(s) ready. Processing will begin automatically.
              </p>
            )}
          </>
        ) : (
          // Confirmation Screen
          <div className="max-w-4xl w-full">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-4">
                <CheckCircle2 className="w-8 h-8 text-green-600" />
              </div>
              <h1 className="text-3xl lg:text-4xl font-medium tracking-tight text-black mb-2">
                Your Personalized Plan is Ready!
              </h1>
              <p className="text-lg text-gray-600">
                Review your analysis and customized learning path below
              </p>
            </div>

            {analysisResult && (
              <div className="space-y-6">
                {/* Profile Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle>Profile Analysis</CardTitle>
                    <CardDescription>
                      {analysisResult.is_duplicate && (
                        <span className="inline-flex items-center gap-1 text-blue-600">
                          <AlertCircle className="w-4 h-4" />
                          Using existing analysis (duplicate detected)
                        </span>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <h3 className="font-semibold text-sm text-gray-700 mb-2">Candidate</h3>
                      <p className="text-lg">{analysisResult.analysis.candidate_name}</p>
                      <p className="text-sm text-gray-600">
                        {analysisResult.analysis.experience_years} years of experience
                      </p>
                    </div>

                    <div>
                      <h3 className="font-semibold text-sm text-gray-700 mb-2">Technical Skills</h3>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.analysis.technical_skills.languages.map((lang) => (
                          <span key={lang} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                            {lang}
                          </span>
                        ))}
                        {analysisResult.analysis.technical_skills.frameworks.slice(0, 4).map((fw) => (
                          <span key={fw} className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-sm">
                            {fw}
                          </span>
                        ))}
                      </div>
                    </div>

                    {analysisResult.analysis.knowledge_gaps && analysisResult.analysis.knowledge_gaps.length > 0 && (
                      <div>
                        <h3 className="font-semibold text-sm text-gray-700 mb-2">areas to Focus On</h3>
                        <ul className="space-y-1">
                          {analysisResult.analysis.knowledge_gaps.slice(0, 3).map((gap, idx) => (
                            <li key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                              <span className="text-orange-500 mt-1">→</span>
                              {gap}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Study Plan Summary */}
                {analysisResult.study_plan && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Your Customized Study Plan</CardTitle>
                      <CardDescription>
                        {analysisResult.study_plan.duration_weeks}-week personalized onboarding path
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {analysisResult.study_plan.plan.weeks.map((week: any) => (
                          <div key={week.weekId} className="p-4 border rounded-lg">
                            <div className="text-sm font-semibold text-gray-700 mb-1">
                              Week {week.weekId}
                            </div>
                            <div className="text-xs text-gray-600 mb-2">{week.title}</div>
                            <div className="flex items-center gap-2 text-xs">
                              <span className="text-gray-500">{week.chapters.length} chapters</span>
                              <span className="text-gray-400">•</span>
                              <span className="text-gray-500">{week.tasks.length} tasks</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Action Buttons */}
                <div className="flex justify-center gap-4 pt-6">
                  <Button
                    variant="outline"
                    onClick={() => {
                      setShowConfirmation(false);
                      setFiles([]);
                      setAnalysisResult(null);
                    }}
                  >
                    Upload Different Resume
                  </Button>
                  <Button
                    onClick={handleConfirm}
                    className="bg-black hover:bg-gray-800 text-white px-8"
                  >
                    Start My Onboarding Journey
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Multi-Step Loader */}
      <MultiStepLoader
        loadingStates={loadingStates}
        loading={loading}
        duration={2000}
        loop={false}
      />

      {/* Close Button */}
      {loading && (
        <button
          className="fixed top-4 right-4 text-black dark:text-white z-120"
          onClick={handleClose}
        >
          <IconSquareRoundedX className="h-10 w-10" />
        </button>
      )}
    </div>
  );
}
