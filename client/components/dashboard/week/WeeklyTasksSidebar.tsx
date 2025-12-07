"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Progress } from "@/components/ui/progress";
import { TaskCard } from "./TaskCard";
import { WeeklyTask } from "@/lib/data/week-content";

interface WeeklyTasksSidebarProps {
  weekId: number;
  tasks: WeeklyTask[];
}

export function WeeklyTasksSidebar({ weekId, tasks }: WeeklyTasksSidebarProps) {
  const router = useRouter();
  const [selectedTask, setSelectedTask] = useState<WeeklyTask | null>(null);

  const handleQuizClick = () => {
    router.push(`/dashboard/week/${weekId}/quiz`);
  };

  return (
    <>
      <aside className="w-80 border-l border-gray-200 bg-white p-6 hidden lg:block">
        <h2 className="text-xl font-semibold text-black mb-6">Weekly Tasks</h2>

        {tasks.length === 0 ? (
          <p className="text-sm text-gray-500">No tasks for this week.</p>
        ) : (
          <div className="space-y-4">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onClick={() => setSelectedTask(task)}
              />
            ))}
          </div>
        )}

        <Button 
          onClick={handleQuizClick}
          className="w-full mt-6 bg-black text-white hover:bg-gray-800"
        >
          Weekly Quiz
        </Button>
      </aside>

      {/* Task Details Modal */}
      <Dialog open={!!selectedTask} onOpenChange={() => setSelectedTask(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{selectedTask?.title}</DialogTitle>
            <DialogDescription>
              Assigned by {selectedTask?.assignedBy} - {selectedTask?.timeAgo}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <p className="text-gray-700">{selectedTask?.description}</p>

            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Progress
                </span>
                <span className="text-sm text-gray-500">
                  {selectedTask?.progress}%
                </span>
              </div>
              <Progress value={selectedTask?.progress ?? 0} className="h-2" />
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}

