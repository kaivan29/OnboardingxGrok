"use client";

import { useParams, redirect } from "next/navigation";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { WeekSidebar } from "@/components/dashboard/week";
import { WeekContentArea } from "@/components/dashboard/week";
import { WeeklyTasksSidebar } from "@/components/dashboard/week";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { getWeekContent, getChapter } from "@/lib/data/week-content";

export default function ChapterPage() {
  const params = useParams();
  const weekId = Number(params.weekId);
  const chapterId = params.chapterId as string;

  const weekContent = getWeekContent(weekId);
  const chapter = getChapter(weekId, chapterId);

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
