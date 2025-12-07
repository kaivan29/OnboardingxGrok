"use client";

import Link from "next/link";
import {
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton,
} from "@/components/ui/sidebar";
import { Chapter } from "@/lib/data/week-content";

interface ChapterNavProps {
  weekId: number;
  chapter: Chapter;
  chapterNumber: number;
  isActive: boolean;
}

export function ChapterNav({
  weekId,
  chapter,
  chapterNumber,
  isActive,
}: ChapterNavProps) {
  const chapterUrl = `/dashboard/week/${weekId}/chapter/${chapter.id}`;

  return (
    <SidebarMenuItem>
      <SidebarMenuButton
        asChild
        isActive={isActive}
        className={
          isActive
            ? "bg-gray-100 font-medium border-l-2 border-black rounded-none"
            : ""
        }
      >
        <Link href={chapterUrl}>
          <div className="flex flex-col items-start gap-0.5">
            <span className="text-sm">
              Chapter {chapterNumber}:{" "}
              {chapter.title.length > 15
                ? chapter.title.slice(0, 15) + "..."
                : chapter.title}
            </span>
            <span className="text-xs text-gray-500">(Reading)</span>
          </div>
        </Link>
      </SidebarMenuButton>

      {/* SubItems - only show when chapter is active */}
      {isActive && chapter.subItems && chapter.subItems.length > 0 && (
        <SidebarMenuSub>
          {chapter.subItems.map((subItem) => (
            <SidebarMenuSubItem key={subItem.id}>
              <SidebarMenuSubButton asChild>
                <a href={`${chapterUrl}#${subItem.id}`}>{subItem.title}</a>
              </SidebarMenuSubButton>
            </SidebarMenuSubItem>
          ))}
        </SidebarMenuSub>
      )}
    </SidebarMenuItem>
  );
}
