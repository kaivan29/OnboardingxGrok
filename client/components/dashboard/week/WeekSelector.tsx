"use client";

import { useRouter } from "next/navigation";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getAllWeeks } from "@/lib/data/week-content";

interface WeekSelectorProps {
  currentWeekId: number;
}

export function WeekSelector({ currentWeekId }: WeekSelectorProps) {
  const router = useRouter();
  const weeks = getAllWeeks();

  const handleWeekChange = (value: string) => {
    const weekId = Number(value);
    router.push(`/dashboard/week/${weekId}`);
  };

  return (
    <Select value={String(currentWeekId)} onValueChange={handleWeekChange}>
      <SelectTrigger className="w-full bg-black text-white hover:bg-gray-800 border-0 font-medium">
        <SelectValue placeholder="Select week" />
      </SelectTrigger>
      <SelectContent>
        {weeks.map((week) => (
          <SelectItem
            key={week.weekId}
            value={String(week.weekId)}
            disabled={week.status === "locked"}
            className={week.status === "locked" ? "opacity-50" : ""}
          >
            Week {week.weekId}: {week.title}
            {week.status === "locked" && " (Locked)"}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
