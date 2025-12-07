"use client";

import { useParams, redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { WeekSidebar } from "@/components/dashboard/week/WeekSidebar";
import { WeekContentArea } from "@/components/dashboard/week/WeekContentArea";
import { WeeklyTasksSidebar } from "@/components/dashboard/week/WeeklyTasksSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { getWeekContent, type WeekContent } from "@/lib/data/week-content";
import { onboardingApi } from "@/lib/api/onboarding";
import { CheckCircle2, Target, BookOpen, Code, Lightbulb, TrendingUp } from "lucide-react";

export default function WeekPage() {
  const params = useParams();
  const weekId = Number(params.weekId);

  const [weekContent, setWeekContent] = useState<WeekContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userName, setUserName] = useState("there");

  useEffect(() => {
    async function loadStudyPlan() {
      try {
        // Get stored IDs from localStorage
        const profileId = localStorage.getItem('profile_id');
        const planId = localStorage.getItem('plan_id');

        if (profileId || planId) {
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
          console.log("📚 Fetching personalized study plan...");
          const studyPlan = await onboardingApi.getStudyPlan({
            profile_id: profileId || undefined,
            plan_id: planId || undefined,
          });

          if (studyPlan.plan && studyPlan.plan.weeks) {
            // Find the specific week
            const week = studyPlan.plan.weeks.find((w: any) => w.weekId === weekId);

            if (week) {
              console.log("✅ Using Grok-generated study plan for week", weekId);
              setWeekContent(week);
              setLoading(false);
              return;
            }
          }
        }

        // Fallback to static data if no personalized plan found
        console.log("ℹ️  No personalized plan found, using static data");
        const staticWeek = getWeekContent(weekId);
        if (staticWeek) {
          setWeekContent(staticWeek);
        } else {
          setError("Week not found");
        }
        setLoading(false);

      } catch (err: any) {
        console.error("Error loading study plan:", err);
        // Fallback to static data on error
        const staticWeek = getWeekContent(weekId);
        if (staticWeek) {
          setWeekContent(staticWeek);
        } else {
          setError("Failed to load week content");
        }
        setLoading(false);
      }
    }

    loadStudyPlan();
  }, [weekId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600 mx-auto mb-6"></div>
            <BookOpen className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-blue-600 w-6 h-6" />
          </div>
          <p className="text-lg font-medium text-gray-700">Loading your personalized curriculum...</p>
          <p className="text-sm text-gray-500 mt-2">Preparing Week {weekId} content</p>
        </div>
      </div>
    );
  }

  if (error || !weekContent) {
    redirect("/dashboard");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <DashboardHeader userFullName={userName} />

      <SidebarProvider defaultOpen={true}>
        <WeekSidebar
          weekId={weekId}
          chapters={weekContent.chapters}
          activeItemId="overview"
        />

        <SidebarInset className="bg-transparent">
          <div className="flex flex-1">
            {/* Main Content */}
            <main className="flex-1 p-6 lg:p-10 overflow-auto">
              {/* Welcome Header */}
              <div className="mb-8">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-4">
                  <TrendingUp className="w-4 h-4" />
                  Week {weekId} of 4
                </div>

                <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-3">
                  {weekContent.title}
                </h1>

                <p className="text-xl text-gray-600 max-w-3xl">
                  Welcome back, {userName}! Let's continue building your expertise. 🚀
                </p>
              </div>

              {/* Week Goal Card */}
              {weekContent.goal && (
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white mb-8 shadow-lg">
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                      <Target className="w-8 h-8" />
                    </div>
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold mb-2">This Week's Goal</h2>
                      <p className="text-blue-50 text-lg leading-relaxed">
                        {weekContent.goal}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Quick Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <BookOpen className="w-5 h-5 text-green-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-600">Chapters</span>
                  </div>
                  <p className="text-3xl font-bold text-gray-900">{weekContent.chapters?.length || 0}</p>
                  <p className="text-sm text-gray-500 mt-1">Reading materials</p>
                </div>

                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <Code className="w-5 h-5 text-purple-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-600">Coding Tasks</span>
                  </div>
                  <p className="text-3xl font-bold text-gray-900">{weekContent.tasks?.length || 0}</p>
                  <p className="text-sm text-gray-500 mt-1">Hands-on practice</p>
                </div>

                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <CheckCircle2 className="w-5 h-5 text-blue-600" />
                    </div>
                    <span className="text-sm font-medium text-gray-600">Quiz Questions</span>
                  </div>
                  <p className="text-3xl font-bold text-gray-900">{(weekContent as any).quiz?.length || 0}</p>
                  <p className="text-sm text-gray-500 mt-1">Test your knowledge</p>
                </div>
              </div>

              {/* Pro Tips Card */}
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 mb-8">
                <div className="flex items-start gap-4">
                  <div className="p-2 bg-amber-100 rounded-lg">
                    <Lightbulb className="w-6 h-6 text-amber-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-amber-900 mb-2">Pro Tips for This Week</h3>
                    <ul className="space-y-2 text-amber-800">
                      <li className="flex items-start gap-2">
                        <span className="text-amber-600 mt-1">•</span>
                        <span>Take breaks between reading sessions - your brain needs time to consolidate</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-amber-600 mt-1">•</span>
                        <span>Don't hesitate to ask questions in Slack or schedule time with your mentor</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-amber-600 mt-1">•</span>
                        <span>Hands-on coding is key - try the tasks even if they seem challenging</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Main Content Card */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-8">
                  <WeekContentArea
                    title="Overview"
                    content={weekContent.overview}
                  />
                </div>
              </div>

              {/* Motivational Footer */}
              <div className="mt-8 text-center p-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl border border-green-100">
                <p className="text-lg font-medium text-gray-700">
                  You're making great progress! 🎉
                </p>
                <p className="text-sm text-gray-600 mt-1">
                  Every expert was once a beginner. Keep learning, keep growing.
                </p>
              </div>
            </main>

            {/* Right Sidebar - Weekly Tasks */}
            <WeeklyTasksSidebar weekId={weekId} tasks={weekContent.tasks} />
          </div>
        </SidebarInset>
      </SidebarProvider>
    </div>
  );
}

