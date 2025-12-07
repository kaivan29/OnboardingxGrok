"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { QuizContainer } from "@/components/quiz";
import { onboardingApi } from "@/lib/api/onboarding";
import type { Quiz, QuizSubmission } from "@/lib/data/quiz";
import { toast } from "sonner";
import { BookOpen, CheckCircle2 } from "lucide-react";

export default function QuizPage() {
  const params = useParams();
  const router = useRouter();
  const weekId = Number(params.weekId);

  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userName, setUserName] = useState("there");

  // Fetch quiz data from study plan
  useEffect(() => {
    let cancelled = false;

    async function fetchQuiz() {
      setLoading(true);
      setError(null);

      try {
        // Get stored IDs from localStorage
        const profileId = localStorage.getItem('profile_id');
        const planId = localStorage.getItem('plan_id');

        if (!profileId && !planId) {
          throw new Error("No study plan found. Please complete onboarding first.");
        }

        // Fetch user profile for name
        if (profileId) {
          try {
            const profile = await onboardingApi.getProfile(profileId);
            if (profile.analysis?.candidate_name) {
              const firstName = profile.analysis.candidate_name.split(' ')[0];
              setUserName(firstName);
            }
          } catch (err) {
            console.error("Failed to load profile:", err);
          }
        }

        // Fetch personalized study plan
        console.log("📚 Fetching quiz from personalized study plan...");
        const studyPlan = await onboardingApi.getStudyPlan({
          profile_id: profileId || undefined,
          plan_id: planId || undefined,
        });

        if (studyPlan.plan && studyPlan.plan.weeks) {
          // Find the specific week
          const week = studyPlan.plan.weeks.find((w: any) => w.weekId === weekId);

          if (week && week.quiz && week.quiz.length > 0) {
            // Convert quiz questions from study plan format to Quiz type
            const quizData: Quiz = {
              id: `week-${weekId}-quiz`,
              weekId: weekId,
              title: `Week ${weekId} Quiz`,
              description: `Test your knowledge of ${week.title}`,
              questions: week.quiz.map((q: any, index: number) => ({
                id: `q${index + 1}`,
                type: "multiple_choice" as const,
                text: q.question,
                options: q.options || [],
                correctAnswer: q.correct_answer,
                explanation: q.explanation,
              })),
            };

            console.log("✅ Loaded quiz with", quizData.questions.length, "questions");
            if (!cancelled) {
              setQuiz(quizData);
            }
          } else {
            throw new Error("No quiz available for this week");
          }
        } else {
          throw new Error("Study plan data not found");
        }
      } catch (err: any) {
        if (!cancelled) {
          setError(err.message || "Unable to load quiz. Please try again.");
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
        // Calculate score
        let correctCount = 0;
        quiz?.questions.forEach((question) => {
          const userAnswer = submission.answers[question.id];
          if (userAnswer === question.correctAnswer) {
            correctCount++;
          }
        });

        const totalQuestions = quiz?.questions.length || 0;
        const score = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;

        console.log("Quiz submitted:", {
          weekId,
          score,
          correctCount,
          totalQuestions,
          submission
        });

        // Show success message with score
        toast.success(
          `Quiz completed! You scored ${score}% (${correctCount}/${totalQuestions} correct)`,
          { duration: 5000 }
        );

        // Redirect back to week page after successful submission
        setTimeout(() => {
          router.push(`/dashboard/week/${weekId}`);
        }, 2000);
      } catch (err) {
        console.error("Failed to submit quiz", err);
        toast.error("Failed to submit quiz. Please try again.");
        throw err; // Re-throw to let QuizContainer know submission failed
      }
    },
    [weekId, router, quiz]
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <DashboardHeader userFullName={userName} />

      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <div className="relative">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600 mx-auto mb-6"></div>
                <CheckCircle2 className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-blue-600 w-6 h-6" />
              </div>
              <p className="text-lg font-medium text-gray-700">Loading your quiz...</p>
              <p className="text-sm text-gray-500 mt-2">Preparing Week {weekId} assessment</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl max-w-md">
              <p className="text-red-600 font-medium">{error}</p>
            </div>
            <button
              onClick={() => router.push(`/dashboard/week/${weekId}`)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Return to Week {weekId}
            </button>
          </div>
        )}

        {/* Quiz Content */}
        {quiz && !loading && !error && (
          <div className="space-y-6">
            {/* Quiz Header */}
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-200">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-blue-100 rounded-xl">
                  <BookOpen className="w-8 h-8 text-blue-600" />
                </div>
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{quiz.title}</h1>
                  <p className="text-gray-600 text-lg">{quiz.description}</p>
                  <div className="mt-4 flex items-center gap-6 text-sm text-gray-500">
                    <span className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4" />
                      {quiz.questions.length} Questions
                    </span>
                    <span>Multiple Choice</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quiz Container */}
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-200">
              <QuizContainer quiz={quiz} onSubmit={handleSubmit} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
