"use client";

import { useFormContext, Controller } from "react-hook-form";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import type { QuizQuestion, QuizFormValues } from "@/lib/data/quiz";

interface FreeResponseQuestionProps {
  /** The question data */
  question: QuizQuestion;
  /** Optional additional className */
  className?: string;
}

/**
 * Renders a free response question with a textarea input.
 * Integrates with react-hook-form via Controller.
 */
export function FreeResponseQuestion({
  question,
  className,
}: FreeResponseQuestionProps) {
  const { control } = useFormContext<QuizFormValues>();

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

      {/* Textarea Input */}
      <Controller
        name={question.id}
        control={control}
        render={({ field }) => (
          <Textarea
            {...field}
            placeholder="Type your answer here..."
            className="min-h-[200px] text-base resize-none border-2 border-gray-200 focus:border-black rounded-lg p-4"
          />
        )}
      />
    </div>
  );
}
