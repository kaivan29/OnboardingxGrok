"use client";

import { useParams, redirect } from "next/navigation";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { WeekSidebar } from "@/components/dashboard/week/WeekSidebar";
import { WeekContentArea } from "@/components/dashboard/week/WeekContentArea";
import { WeeklyTasksSidebar } from "@/components/dashboard/week/WeeklyTasksSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { getWeekContent } from "@/lib/data/week-content";

export default function WeekPage() {
  const params = useParams();
  const weekId = Number(params.weekId);

  const weekContent = getWeekContent(weekId);

  if (!weekContent) {
    redirect("/dashboard");
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader userFullName="Alex Chen" />

      <SidebarProvider defaultOpen={true}>
        <WeekSidebar
          weekId={weekId}
          chapters={weekContent.chapters}
          activeItemId="overview"
        />

        <SidebarInset className="bg-gray-50">
          <div className="flex flex-1">
            {/* Main Content */}
            <main className="flex-1 p-8 overflow-auto">
              <WeekContentArea
                title="Overview"
                content={weekContent.overview}
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
