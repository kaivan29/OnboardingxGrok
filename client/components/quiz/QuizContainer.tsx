"use client";

import { useState, useCallback } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { QuizProgress } from "./QuizProgress";
import { MultipleChoiceQuestion } from "./MultipleChoiceQuestion";
import { FreeResponseQuestion } from "./FreeResponseQuestion";
import { QuizNavigation } from "./QuizNavigation";
import type { Quiz, QuizFormValues, QuizSubmission } from "@/lib/data/quiz";
import { cn } from "@/lib/utils";

interface QuizContainerProps {
  /** The quiz data */
  quiz: Quiz;
  /** Handler called when quiz is submitted */
  onSubmit: (submission: QuizSubmission) => Promise<void>;
  /** Optional additional className */
  className?: string;
}

/**
 * Creates a dynamic zod schema based on quiz questions.
 * All questions are required.
 */
function createQuizSchema(quiz: Quiz) {
  const shape: Record<string, z.ZodString> = {};

  for (const question of quiz.questions) {
    shape[question.id] = z.string().min(1, "This question is required");
  }

  return z.object(shape);
}

/**
 * Main quiz container that orchestrates the multi-step form.
 * Manages question navigation, form state, and submission.
 */
export function QuizContainer({
  quiz,
  onSubmit,
  className,
}: QuizContainerProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const totalQuestions = quiz.questions.length;
  const currentQuestion = quiz.questions[currentIndex];

  // Create form with dynamic schema
  const schema = createQuizSchema(quiz);
  const methods = useForm<QuizFormValues>({
    resolver: zodResolver(schema),
    defaultValues: quiz.questions.reduce(
      (acc, q) => ({ ...acc, [q.id]: "" }),
      {} as QuizFormValues
    ),
    mode: "onChange",
  });

  const { handleSubmit, trigger } = methods;

  // Navigate to previous question
  const handleBack = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  }, [currentIndex]);

  // Navigate to next question or submit
  const handleNext = useCallback(async () => {
    // Validate current question before proceeding
    const isValid = await trigger(currentQuestion.id);

    if (!isValid) {
      return;
    }

    if (currentIndex < totalQuestions - 1) {
      // Go to next question
      setCurrentIndex((prev) => prev + 1);
    } else {
      // Submit the quiz
      handleSubmit(async (data) => {
        setIsSubmitting(true);
        try {
          const submission: QuizSubmission = {
            quizId: quiz.id,
            answers: data,
          };
          await onSubmit(submission);
        } finally {
          setIsSubmitting(false);
        }
      })();
    }
  }, [currentIndex, totalQuestions, currentQuestion, trigger, handleSubmit, quiz.id, onSubmit]);

  return (
    <FormProvider {...methods}>
      <div className={cn("w-full max-w-2xl mx-auto", className)}>
        {/* Progress Bar */}
        <QuizProgress
          currentQuestion={currentIndex + 1}
          totalQuestions={totalQuestions}
          className="mb-12"
        />

        {/* Question Content */}
        <div className="min-h-[300px] mb-12">
          {currentQuestion.type === "multiple_choice" ? (
            <MultipleChoiceQuestion
              key={currentQuestion.id}
              question={currentQuestion}
            />
          ) : (
            <FreeResponseQuestion
              key={currentQuestion.id}
              question={currentQuestion}
            />
          )}
        </div>

        {/* Navigation */}
        <QuizNavigation
          currentIndex={currentIndex}
          totalQuestions={totalQuestions}
          onBack={handleBack}
          onNext={handleNext}
          isSubmitting={isSubmitting}
        />
      </div>
    </FormProvider>
  );
}
