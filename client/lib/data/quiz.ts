// ============================================================================
// Quiz Types
// ============================================================================

export type QuestionType = "multiple_choice" | "free_response";

export interface QuizOption {
  id: string;
  label: string; // e.g., "A", "B", "C", "D"
  text: string;
}

export interface QuizQuestion {
  id: string;
  questionNumber: number;
  type: QuestionType;
  question: string;
  options?: QuizOption[]; // Only for multiple_choice
}

export interface Quiz {
  id: string;
  weekId: number;
  title: string;
  questions: QuizQuestion[];
}

export interface QuizSubmission {
  quizId: string;
  answers: Record<string, string>; // questionId -> answer
}

// Form values type for react-hook-form
export type QuizFormValues = Record<string, string>;

// ============================================================================
// Mock Quiz Data
// ============================================================================

export const mockQuizWeek1: Quiz = {
  id: "quiz-week-1",
  weekId: 1,
  title: "Week 1: Foundations & Setup Quiz",
  questions: [
    // Multiple Choice Questions (1-3)
    {
      id: "q1",
      questionNumber: 1,
      type: "multiple_choice",
      question: "What is the primary purpose of a Pull Request (PR) review?",
      options: [
        {
          id: "q1-a",
          label: "A",
          text: "To facilitate knowledge sharing and collaboration among team members.",
        },
        {
          id: "q1-b",
          label: "B",
          text: "To ensure code adheres to style guidelines and best practices.",
        },
        {
          id: "q1-c",
          label: "C",
          text: "To find bugs before they reach production.",
        },
        {
          id: "q1-d",
          label: "D",
          text: "All of the above.",
        },
      ],
    },
    {
      id: "q2",
      questionNumber: 2,
      type: "multiple_choice",
      question:
        "Which version control branching strategy involves creating a new branch for each feature?",
      options: [
        {
          id: "q2-a",
          label: "A",
          text: "Trunk-based development",
        },
        {
          id: "q2-b",
          label: "B",
          text: "Feature branching",
        },
        {
          id: "q2-c",
          label: "C",
          text: "GitFlow",
        },
        {
          id: "q2-d",
          label: "D",
          text: "Mainline development",
        },
      ],
    },
    {
      id: "q3",
      questionNumber: 3,
      type: "multiple_choice",
      question:
        "What is the recommended approach when you encounter a bug in someone else's code?",
      options: [
        {
          id: "q3-a",
          label: "A",
          text: "Fix it silently without telling anyone.",
        },
        {
          id: "q3-b",
          label: "B",
          text: "File a detailed bug report and optionally propose a fix.",
        },
        {
          id: "q3-c",
          label: "C",
          text: "Ignore it since it's not your responsibility.",
        },
        {
          id: "q3-d",
          label: "D",
          text: "Rewrite the entire module from scratch.",
        },
      ],
    },
    // Free Response Questions (4-5)
    {
      id: "q4",
      questionNumber: 4,
      type: "free_response",
      question:
        "Describe the key differences between active recall and passive reading as learning strategies. How would you apply active recall in your onboarding process?",
    },
    {
      id: "q5",
      questionNumber: 5,
      type: "free_response",
      question:
        "What steps would you take to set up an effective local development environment for a new project? Include considerations for both physical workspace and digital tools.",
    },
  ],
};

// Map of all quizzes by weekId for easy lookup
export const quizzesByWeek: Record<number, Quiz> = {
  1: mockQuizWeek1,
};

// ============================================================================
// Helper Functions
// ============================================================================

export function getQuizByWeekId(weekId: number): Quiz | undefined {
  return quizzesByWeek[weekId];
}

export function getTotalQuestions(quiz: Quiz): number {
  return quiz.questions.length;
}

export function getQuestionByIndex(
  quiz: Quiz,
  index: number
): QuizQuestion | undefined {
  return quiz.questions[index];
}
