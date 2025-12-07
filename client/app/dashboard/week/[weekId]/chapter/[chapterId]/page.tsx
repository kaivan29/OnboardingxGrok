"use client";

import { useParams, redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { WeekSidebar } from "@/components/dashboard/week";
import { WeekContentArea } from "@/components/dashboard/week";
import { WeeklyTasksSidebar } from "@/components/dashboard/week";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { getWeekContent, getChapter, type Chapter, type WeekContent } from "@/lib/data/week-content";
import { api } from "@/lib/api-client";

export default function ChapterPage() {
  const params = useParams();
  const weekId = Number(params.weekId);
  const chapterId = params.chapterId as string;

  const [weekContent, setWeekContent] = useState<WeekContent | null>(null);
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadContent() {
      try {
        // Try to get profile_id from localStorage
        const profileId = localStorage.getItem('profile_id');

        if (profileId) {
          // Fetch personalized study plan from API
          console.log("📚 Fetching personalized study plan for profile:", profileId);
          const response = await api.get<any>(`/getStudyPlan/${profileId}`);

          if (response.data && response.data.plan && response.data.plan.weeks) {
            // Find the specific week
            const week = response.data.plan.weeks.find((w: any) => w.weekId === weekId);

            if (week) {
              // Find the specific chapter
              const chap = week.chapters.find((c: any) => c.id === chapterId);

              if (chap) {
                console.log("✅ Using personalized chapter:", chapterId);
                setWeekContent(week);
                setChapter(chap);
                setLoading(false);
                return;
              }
            }
          }
        }

        // Fallback to static data
        console.log("ℹ️  Using static data for fallback");
        const staticWeek = getWeekContent(weekId);
        const staticChapter = getChapter(weekId, chapterId);

        if (staticWeek && staticChapter) {
          setWeekContent(staticWeek);
          setChapter(staticChapter);
        }
        setLoading(false);

      } catch (err) {
        console.error("Error loading content:", err);
        // Fallback to static data on error
        const staticWeek = getWeekContent(weekId);
        const staticChapter = getChapter(weekId, chapterId);

        if (staticWeek && staticChapter) {
          setWeekContent(staticWeek);
          setChapter(staticChapter);
        }
        setLoading(false);
      }
    }

    loadContent();
  }, [weekId, chapterId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-gray-600">Loading chapter content...</p>
        </div>
      </div>
    );
  }

  if (!weekContent) {
    redirect("/dashboard");
  }

  if (!chapter) {
    redirect(`/dashboard/week/${weekId}`);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader userFullName="Alex Chen" />

      <SidebarProvider defaultOpen={true}>
        <WeekSidebar
          weekId={weekId}
          chapters={weekContent.chapters}
          activeItemId={chapterId}
        />

        <SidebarInset className="bg-gray-50">
          <div className="flex flex-1">
            {/* Main Content */}
            <main className="flex-1 p-8 overflow-auto">
              <WeekContentArea
                title={chapter.title}
                content={chapter.content}
                subItems={chapter.subItems}
              />
            </main>

            {/* Right Sidebar - Weekly Tasks */}
            <WeeklyTasksSidebar tasks={weekContent.tasks} />
          </div>
        </SidebarInset>
      </SidebarProvider>
    </div>
  );
}
