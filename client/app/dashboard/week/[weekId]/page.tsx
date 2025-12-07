"use client";

import { useParams, redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { WeekSidebar } from "@/components/dashboard/week/WeekSidebar";
import { WeekContentArea } from "@/components/dashboard/week/WeekContentArea";
import { WeeklyTasksSidebar } from "@/components/dashboard/week/WeeklyTasksSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { getWeekContent, type WeekContent } from "@/lib/data/week-content";
import { api } from "@/lib/api-client";

export default function WeekPage() {
  const params = useParams();
  const weekId = Number(params.weekId);

  const [weekContent, setWeekContent] = useState<WeekContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStudyPlan() {
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
              console.log("✅ Using personalized study plan for week", weekId);
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

      } catch (err) {
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
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your personalized content...</p>
        </div>
      </div>
    );
  }

  if (error || !weekContent) {
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
