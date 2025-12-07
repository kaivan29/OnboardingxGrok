"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Progress } from "@/components/ui/progress";
import { Brain, Code2, GitBranch } from "lucide-react";
import {
  WeeklyModuleCard,
  ModuleStatus,
} from "@/components/dashboard/WeeklyModuleCard";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { onboardingApi, StudyPlan, UserProfile } from "@/lib/api/onboarding";
import { toast } from "sonner";

interface Week {
  weekId: number;
  title: string;
  description: string;
  chapters: any[];
  tasks: any[];
}

export default function DashboardPage() {
  const router = useRouter();
  const [userFullName, setUserFullName] = useState("User");
  const [modules, setModules] = useState<{ week: number; title: string; status: ModuleStatus }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [courseProgress, setCourseProgress] = useState(0);
  const [tasksDue, setTasksDue] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadDashboardData() {
      setLoading(true);
      setError(null);

      try {
        // Get stored IDs from localStorage
        const profileId = localStorage.getItem('profile_id');
        const planId = localStorage.getItem('plan_id');

        if (!profileId && !planId) {
          // No profile found, redirect to onboarding
          toast.error("Please upload your resume first");
          router.push("/onboarding");
          return;
        }

        // Fetch user profile to get name
        if (profileId) {
          try {
            const profile: UserProfile = await onboardingApi.getProfile(profileId);
            if (!cancelled && profile.analysis?.candidate_name) {
              setUserFullName(profile.analysis.candidate_name);
            }
          } catch (err) {
            console.error("Failed to load profile:", err);
          }
        }

        // Fetch study plan
        const studyPlan: StudyPlan = await onboardingApi.getStudyPlan({
          profile_id: profileId || undefined,
          plan_id: planId || undefined,
        });

        if (!cancelled) {
          // Convert study plan weeks to module format
          const moduleData = studyPlan.plan.weeks.map((week: Week, index: number) => {
            // Determine status based on week number
            let status: ModuleStatus;
            if (index === 0) {
              status = "continue"; // First week is current
            } else if (index < studyPlan.plan.weeks.length - 1) {
              status = "start"; // Middle weeks
            } else {
              status = "locked"; // Last week
            }

            return {
              week: week.weekId,
              title: week.title,
              status,
            };
          });

          setModules(moduleData);

          // Calculate progress (first week = in progress)
          const progressPercent = Math.round((1 / studyPlan.plan.weeks.length) * 30);
          setCourseProgress(progressPercent);

          // Count tasks from first week
          if (studyPlan.plan.weeks.length > 0) {
            setTasksDue(studyPlan.plan.weeks[0].tasks.length);
          }
        }
      } catch (err: any) {
        if (!cancelled) {
          console.error("Failed to load dashboard data:", err);
          const errorMsg = err.response?.data?.detail || err.message || "Failed to load your study plan";
          setError(errorMsg);
          toast.error(errorMsg);

          // If profile/plan not found, redirect to onboarding
          if (err.response?.status === 404) {
            setTimeout(() => router.push("/onboarding"), 2000);
          }
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadDashboardData();
    return () => {
      cancelled = true;
    };
  }, [router]);

  const userFirstName = userFullName.split(" ")[0] ?? userFullName;

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader userFullName={userFullName} />

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 lg:px-12 py-12">
        {/* Welcome Section */}
        <div className="flex items-center gap-12 mb-16">
          {/* Illustration */}
          <div className="hidden lg:flex items-center justify-center w-64 h-48 relative">
            <div className="absolute w-24 h-24 border-2 border-black rounded-xl transform -rotate-12 bg-white flex items-center justify-center">
              <Code2 className="w-10 h-10 text-gray-800" />
            </div>
            <div className="absolute top-0 right-8 w-16 h-16 border-2 border-black rounded-lg transform rotate-12 bg-white flex items-center justify-center">
              <GitBranch className="w-8 h-8 text-gray-800" />
            </div>
            <div className="absolute bottom-4 left-8 w-20 h-20 border-2 border-black rounded-full bg-white flex items-center justify-center">
              <Brain className="w-10 h-10 text-gray-800" />
            </div>
            {/* Decorative arrows */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30">
              <path
                d="M40,80 Q60,40 100,60"
                fill="none"
                stroke="black"
                strokeWidth="2"
              />
              <path
                d="M150,30 L160,50"
                fill="none"
                stroke="black"
                strokeWidth="2"
              />
            </svg>
          </div>

          {/* Welcome Text */}
          <div className="flex-1">
            <h1 className="text-4xl font-semibold text-black mb-3">
              Welcome back, {userFirstName}!
            </h1>
            <p className="text-gray-600 text-lg mb-6">
              Continue your learning journey today. You have{" "}
              <span className="font-semibold">{tasksDue} tasks due</span> this
              week.
            </p>

            {/* Progress Bar */}
            <div className="max-w-md">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Course Progress:
                </span>
                <span className="text-sm text-gray-600">
                  {courseProgress}% complete
                </span>
              </div>
              <Progress value={courseProgress} className="h-3" />
            </div>
          </div>
        </div>

        {/* Weekly Modules Section */}
        <section>
          <h2 className="text-2xl font-semibold text-black mb-6">
            Your Weekly Modules
          </h2>

          {loading && (
            <p className="text-sm text-gray-600 mb-4">Loading your personalized study plan...</p>
          )}
          {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {modules.map((module) => (
              <WeeklyModuleCard
                key={module.week}
                week={module.week}
                title={module.title}
                status={module.status}
              />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
