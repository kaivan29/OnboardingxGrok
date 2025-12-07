"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { QuizContainer } from "@/components/quiz";
import { quizApi } from "@/lib/api/quiz";
import type { Quiz, QuizSubmission } from "@/lib/data/quiz";
import { toast } from "sonner";

export default function QuizPage() {
  const params = useParams();
  const router = useRouter();
  const weekId = Number(params.weekId);

  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch quiz data
  useEffect(() => {
    let cancelled = false;

    async function fetchQuiz() {
      setLoading(true);
      setError(null);

      try {
        const response = await quizApi.getQuiz(weekId);
        if (!cancelled) {
          setQuiz(response.data);
        }
      } catch (err) {
        if (!cancelled) {
          setError("Unable to load quiz. Please try again.");
          console.error("Failed to load quiz", err);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchQuiz();
    return () => {
      cancelled = true;
    };
  }, [weekId]);

  // Handle quiz submission
  const handleSubmit = useCallback(
    async (submission: QuizSubmission) => {
      try {
        await quizApi.submitQuiz(submission);
        toast.success("Quiz submitted successfully!");
        // Redirect back to week page after successful submission
        router.push(`/dashboard/week/${weekId}`);
      } catch (err) {
        console.error("Failed to submit quiz", err);
        toast.error("Failed to submit quiz. Please try again.");
        throw err; // Re-throw to let QuizContainer know submission failed
      }
    },
    [weekId, router]
  );

  return (
    <div className="min-h-screen bg-white">
      <DashboardHeader userFullName="Alex Chen" />

      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center min-h-[400px]">
            <p className="text-gray-600">Loading quiz...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
            <p className="text-red-600">{error}</p>
            <button
              onClick={() => router.push(`/dashboard/week/${weekId}`)}
              className="text-gray-600 underline hover:text-gray-800"
            >
              Return to week page
            </button>
          </div>
        )}

        {/* Quiz Content */}
        {quiz && !loading && !error && (
          <QuizContainer quiz={quiz} onSubmit={handleSubmit} />
        )}
      </main>
    </div>
  );
}
