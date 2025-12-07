"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";
import { WeekSelector } from "./WeekSelector";
import { ChapterNav } from "./ChapterNav";
import { Chapter } from "@/lib/data/week-content";

interface WeekSidebarProps {
  weekId: number;
  chapters: Chapter[];
  activeItemId: string; // "overview" or chapter id
}

export function WeekSidebar({
  weekId,
  chapters,
  activeItemId,
}: WeekSidebarProps) {
  return (
    <Sidebar collapsible="none" className="border-r border-gray-200 bg-white">
      <SidebarHeader className="border-b border-gray-200 p-4">
        <WeekSelector currentWeekId={weekId} />
      </SidebarHeader>

      <SidebarContent className="p-2">
        <SidebarMenu>
          {/* Overview Item */}
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={activeItemId === "overview"}
              className={
                activeItemId === "overview"
                  ? "bg-gray-100 font-medium border-l-2 border-black rounded-none"
                  : ""
              }
            >
              <a href={`/dashboard/week/${weekId}`}>Overview</a>
            </SidebarMenuButton>
          </SidebarMenuItem>

          {/* Chapter Navigation */}
          {chapters.map((chapter, index) => (
            <ChapterNav
              key={chapter.id}
              weekId={weekId}
              chapter={chapter}
              chapterNumber={index + 1}
              isActive={activeItemId === chapter.id}
            />
          ))}
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  );
}
