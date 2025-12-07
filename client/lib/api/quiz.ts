import { api } from "@/lib/api-client";
import type { Quiz, QuizSubmission } from "@/lib/data/quiz";
import { getQuizByWeekId } from "@/lib/data/quiz";

export const quizApi = {
  /**
   * Fetch quiz for a specific week
   * Currently uses mock data adapter, will use real endpoint when available
   */
  getQuiz: (weekId: number) =>
    api.get<Quiz>(`/quiz/${weekId}`, {
      adapter: async (config) => {
        // Mock adapter - returns local data until backend is ready
        const quiz = getQuizByWeekId(weekId);
        if (!quiz) {
          return Promise.reject({
            response: { status: 404, data: { message: "Quiz not found" } },
            config,
          });
        }
        return Promise.resolve({
          data: quiz,
          status: 200,
          statusText: "OK",
          headers: {},
          config,
        });
      },
    }),

  /**
   * Submit quiz answers
   * Currently mocked, will use real endpoint when available
   */
  submitQuiz: (submission: QuizSubmission) =>
    api.post<{ success: boolean }>("/quiz/submit", submission, {
      adapter: async (config) => {
        // Mock adapter - simulates successful submission
        console.log("Quiz submission:", submission);
        return Promise.resolve({
          data: { success: true },
          status: 200,
          statusText: "OK",
          headers: {},
          config,
        });
      },
    }),
};
