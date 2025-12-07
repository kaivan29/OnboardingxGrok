"use client";

import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface QuizProgressProps {
  /** Current question number (1-indexed) */
  currentQuestion: number;
  /** Total number of questions */
  totalQuestions: number;
  /** Optional additional className */
  className?: string;
}

/**
 * Progress bar component for the quiz.
 * Shows a visual progress indicator and "Question X of Y" text.
 */
export function QuizProgress({
  currentQuestion,
  totalQuestions,
  className,
}: QuizProgressProps) {
  const progressPercent = (currentQuestion / totalQuestions) * 100;

  return (
    <div className={cn("w-full", className)}>
      <Progress
        value={progressPercent}
        className="h-2 bg-gray-200"
        // Custom styling to match the reference design (black progress bar)
      />
      <p className="mt-2 text-sm text-gray-600">
        Question {currentQuestion} of {totalQuestions}
      </p>
    </div>
  );
}
