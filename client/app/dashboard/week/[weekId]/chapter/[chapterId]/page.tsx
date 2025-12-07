"use client";

import { useParams, redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { WeekSidebar } from "@/components/dashboard/week/WeekSidebar";
import { WeekContentArea } from "@/components/dashboard/week/WeekContentArea";
import { WeeklyTasksSidebar } from "@/components/dashboard/week/WeeklyTasksSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { getWeekContent, getChapter, type Chapter, type WeekContent } from "@/lib/data/week-content";
import { onboardingApi } from "@/lib/api/onboarding";
import { BookOpen } from "lucide-react";

export default function ChapterPage() {
  const params = useParams();
  const weekId = Number(params.weekId);
  const chapterId = params.chapterId as string;

  const [weekContent, setWeekContent] = useState<WeekContent | null>(null);
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userName, setUserName] = useState("there");

  useEffect(() => {
    async function loadContent() {
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
              // Find the specific chapter
              const chap = week.chapters.find((c: any) => c.id === chapterId);

              if (chap) {
                console.log("✅ Using Grok-generated study plan for chapter:", chapterId);
                setWeekContent(week);
                setChapter(chap);
                setLoading(false);
                return;
              }
            }
          }
        }

        // Fallback to static data if no personalized plan found
        console.log("ℹ️  No personalized plan found, using static data");
        const staticWeek = getWeekContent(weekId);
        const staticChapter = getChapter(weekId, chapterId);

        if (staticWeek && staticChapter) {
          setWeekContent(staticWeek);
          setChapter(staticChapter);
        } else {
          setError("Chapter not found");
        }
        setLoading(false);

      } catch (err: any) {
        console.error("Error loading content:", err);
        // Fallback to static data on error
        const staticWeek = getWeekContent(weekId);
        const staticChapter = getChapter(weekId, chapterId);

        if (staticWeek && staticChapter) {
          setWeekContent(staticWeek);
          setChapter(staticChapter);
        } else {
          setError("Failed to load chapter content");
        }
        setLoading(false);
      }
    }

    loadContent();
  }, [weekId, chapterId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600 mx-auto mb-6"></div>
            <BookOpen className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-blue-600 w-6 h-6" />
          </div>
          <p className="text-lg font-medium text-gray-700">Loading chapter content...</p>
          <p className="text-sm text-gray-500 mt-2">Preparing your learning materials</p>
        </div>
      </div>
    );
  }

  if (error || !weekContent) {
    redirect("/dashboard");
  }

  if (!chapter) {
    redirect(`/dashboard/week/${weekId}`);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <DashboardHeader userFullName={userName} />

      <SidebarProvider defaultOpen={true}>
        <WeekSidebar
          weekId={weekId}
          chapters={weekContent.chapters}
          activeItemId={chapterId}
        />

        <SidebarInset className="bg-transparent">
          <div className="flex flex-1">
            {/* Main Content */}
            <main className="flex-1 p-6 lg:p-10 overflow-auto">
              <WeekContentArea
                title={chapter.title}
                content={chapter.content}
                subItems={chapter.subItems}
              />
            </main>

            {/* Right Sidebar - Weekly Tasks */}
            <WeeklyTasksSidebar weekId={weekId} tasks={weekContent.tasks} />
          </div>
        </SidebarInset>
      </SidebarProvider>
    </div>
  );
}
