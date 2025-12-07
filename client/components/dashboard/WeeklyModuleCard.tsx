"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

export type ModuleStatus = "completed" | "continue" | "start" | "locked";

interface WeeklyModuleCardProps {
  week: number;
  title: string;
  status: ModuleStatus;
}

const STATUS: Record<
  ModuleStatus,
  {
    label: string;
    buttonText: string;
    buttonVariant: "default" | "outline";
    showIcon: boolean;
    disabled?: boolean;
  }
> = {
  completed: { label: "Completed", buttonText: "Review", buttonVariant: "outline", showIcon: true },
  continue: { label: "Continue", buttonText: "Continue", buttonVariant: "outline", showIcon: false },
  start: { label: "Start", buttonText: "Start", buttonVariant: "default", showIcon: false },
  locked: { label: "Locked", buttonText: "Locked", buttonVariant: "outline", showIcon: false, disabled: true },
};

export function WeeklyModuleCard({ week, title, status }: WeeklyModuleCardProps) {
  const router = useRouter();
  const config = STATUS[status];

  return (
    <div className="flex flex-col justify-between p-6 bg-white border border-gray-200 rounded-xl min-h-[200px]">
      <div>
        <span className="inline-block px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-full mb-4">
          Week {week}
        </span>

        <h3 className="text-xl font-semibold text-black leading-tight">{title}</h3>

        <div className="flex items-center gap-1.5 mt-2">
          <span className="text-sm text-gray-600">{config.label}</span>
          {config.showIcon && <Check className="w-4 h-4 text-green-500" />}
        </div>
      </div>

      <Button
        variant={config.buttonVariant}
        disabled={config.disabled}
        className={cn(
          "w-full mt-4 rounded-lg",
          config.buttonVariant === "default" && "bg-black text-white hover:bg-gray-800"
        )}
        onClick={() => router.push(`/dashboard/week/${week}`)}
      >
        {config.buttonText}
      </Button>
    </div>
  );
}
