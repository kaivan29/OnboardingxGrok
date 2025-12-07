"use client";

import { Progress } from "@/components/ui/progress";
import { WeeklyTask } from "@/lib/data/week-content";

interface TaskCardProps {
  task: WeeklyTask;
  onClick: () => void;
}

export function TaskCard({ task, onClick }: TaskCardProps) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all"
    >
      <h4 className="font-semibold text-black mb-1">{task.title}</h4>
      <p className="text-sm text-gray-500 mb-3">
        Assigned by {task.assignedBy} - {task.timeAgo}
      </p>
      <Progress value={task.progress} className="h-2" />
    </button>
  );
}
