"use client";
import React, { useState, useCallback } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { MultiStepLoader } from "@/components/ui/multi-step-loader";
import { IconSquareRoundedX } from "@tabler/icons-react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { onboardingApi } from "@/lib/api/onboarding";
import { toast } from "sonner";

const loadingStates = [
  { text: "Uploading resume..." },
  { text: "Analyzing your experience" },
  { text: "Identifying relevant skills" },
  { text: "Mapping to codebase structure" },
  { text: "Generating personalized tutorial" },
  { text: "Preparing your dashboard" },
];

export default function OnboardingPage() {
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

  const handleFileUpload = useCallback(async (uploadedFiles: File[]) => {
    if (uploadedFiles.length === 0) return;

    setFiles(uploadedFiles);

    try {
      // Upload the resume
      const uploadResponse = await onboardingApi.uploadResume(uploadedFiles[0]);
      console.log("Upload response:", uploadResponse);

      // Start the loader animation
      setLoading(true);

      // TODO: Poll for status updates or use WebSocket for real-time updates
      // For now, the multi-step loader will animate through all steps
    } catch (err) {
      console.error("Upload failed:", err);
      toast.error("Failed to upload resume. Please try again.");
      setLoading(false);
    }
  }, []);

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
        <div className="max-w-2xl w-full text-center mb-12">
          <h1 className="text-4xl lg:text-5xl font-medium tracking-tight text-black mb-4">
            Upload Your Resume
          </h1>
          <p className="text-lg text-gray-600 leading-relaxed">
            We&apos;ll analyze your experience and generate a personalized
            codebase tutorial tailored to your background.
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
