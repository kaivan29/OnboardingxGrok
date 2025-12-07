"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface QuizNavigationProps {
  /** Current question index (0-indexed) */
  currentIndex: number;
  /** Total number of questions */
  totalQuestions: number;
  /** Handler for going to previous question */
  onBack: () => void;
  /** Handler for going to next question or submitting */
  onNext: () => void;
  /** Whether the form is currently submitting */
  isSubmitting?: boolean;
  /** Optional additional className */
  className?: string;
}

/**
 * Navigation buttons for the quiz (Back/Next/Submit).
 * Styled to match the reference design with rounded black buttons.
 */
export function QuizNavigation({
  currentIndex,
  totalQuestions,
  onBack,
  onNext,
  isSubmitting = false,
  className,
}: QuizNavigationProps) {
  const isFirstQuestion = currentIndex === 0;
  const isLastQuestion = currentIndex === totalQuestions - 1;

  return (
    <div className={cn("flex items-center justify-end gap-3", className)}>
      {/* Back Button */}
      <Button
        type="button"
        variant="default"
        onClick={onBack}
        disabled={isFirstQuestion || isSubmitting}
        className={cn(
          "px-6 py-2 rounded-full font-medium",
          "bg-black text-white hover:bg-gray-800",
          "disabled:bg-gray-300 disabled:text-gray-500"
        )}
      >
        Back
      </Button>

      {/* Next/Submit Button */}
      <Button
        type="button"
        variant="default"
        onClick={onNext}
        disabled={isSubmitting}
        className={cn(
          "px-6 py-2 rounded-full font-medium",
          "bg-black text-white hover:bg-gray-800",
          "disabled:bg-gray-300 disabled:text-gray-500"
        )}
      >
        {isSubmitting ? (
          "Submitting..."
        ) : isLastQuestion ? (
          "Submit"
        ) : (
          <>
            Next <ArrowRight className="w-4 h-4 ml-1" />
          </>
        )}
      </Button>
    </div>
  );
}
