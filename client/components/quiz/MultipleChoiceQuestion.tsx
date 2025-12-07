"use client";

import { useFormContext, Controller } from "react-hook-form";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";
import type { QuizQuestion, QuizFormValues } from "@/lib/data/quiz";

interface MultipleChoiceQuestionProps {
  /** The question data */
  question: QuizQuestion;
  /** Optional additional className */
  className?: string;
}

/**
 * Renders a multiple choice question with selectable option cards.
 * Integrates with react-hook-form via Controller.
 */
export function MultipleChoiceQuestion({
  question,
  className,
}: MultipleChoiceQuestionProps) {
  const { control } = useFormContext<QuizFormValues>();

  if (!question.options) {
    return null;
  }

  return (
    <div className={cn("w-full", className)}>
      {/* Question Header */}
      <div className="flex items-start gap-3 mb-8">
        <span className="shrink-0 w-8 h-8 bg-black text-white rounded-md flex items-center justify-center text-sm font-semibold">
          {question.questionNumber}
        </span>
        <h2 className="text-2xl font-semibold text-black leading-tight">
          {question.questionNumber}. {question.question}
        </h2>
      </div>

      {/* Options */}
      <Controller
        name={question.id}
        control={control}
        render={({ field }) => (
          <div className="space-y-3">
            {question.options!.map((option) => {
              const isSelected = field.value === option.id;

              return (
                <button
                  key={option.id}
                  type="button"
                  onClick={() => field.onChange(option.id)}
                  className={cn(
                    "w-full flex items-center gap-4 p-4 rounded-lg border-2 transition-all text-left",
                    isSelected
                      ? "border-black bg-black text-white"
                      : "border-gray-200 bg-white hover:border-gray-300"
                  )}
                >
                  {/* Selection Indicator */}
                  <span
                    className={cn(
                      "shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center",
                      isSelected
                        ? "border-white bg-white"
                        : "border-gray-300 bg-white"
                    )}
                  >
                    {isSelected && (
                      <Check className="w-4 h-4 text-black" strokeWidth={3} />
                    )}
                  </span>

                  {/* Option Label & Text */}
                  <span className="flex-1">
                    <span
                      className={cn(
                        "font-medium",
                        isSelected ? "text-white" : "text-gray-500"
                      )}
                    >
                      {option.label}.{" "}
                    </span>
                    <span
                      className={cn(
                        isSelected ? "text-white" : "text-gray-900"
                      )}
                    >
                      {option.text}
                    </span>
                  </span>
                </button>
              );
            })}
          </div>
        )}
      />
    </div>
  );
}
