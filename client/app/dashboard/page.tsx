"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { ChevronDown, Brain, Code2, GitBranch } from "lucide-react";
import { WeeklyModuleCard, ModuleStatus } from "@/components/dashboard/WeeklyModuleCard";
import { api } from "@/lib/api-client";

// Sample module data - in production, this would come from API
const weeklyModules: { week: number; title: string; status: ModuleStatus }[] = [
  { week: 1, title: "Foundations & Setup", status: "completed" },
  { week: 2, title: "Data Structures", status: "continue" },
  { week: 3, title: "Algorithms", status: "start" },
  { week: 4, title: "Summary", status: "locked" },
];

export default function DashboardPage() {
  const userName = "Alex";
  const courseProgress = 45;
  const tasksDue = 3;

  const [modules, setModules] = useState<typeof weeklyModules>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchModules() {
      setLoading(true);
      setError(null);

      try {
        // Mocked API call using the shared api client; replace adapter with real endpoint later.
        const response = await api.get<typeof weeklyModules>("/weekly-modules", {
          adapter: async (config) =>
            Promise.resolve({
              data: weeklyModules,
              status: 200,
              statusText: "OK",
              headers: {},
              config,
            }),
        });

        if (!cancelled) {
          setModules(response.data);
        }
      } catch (err) {
        if (!cancelled) {
          setError("Unable to load modules. Please try again.");
          console.error("Failed to load weekly modules", err);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchModules();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="flex h-14 w-full items-center justify-between border-b border-gray-200 px-6 lg:px-12 bg-white">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-3">
            <div className="grid grid-cols-3 gap-1 w-6 h-6">
              {[...Array(9)].map((_, i) => (
                <div
                  key={i}
                  className={`w-1 h-1 rounded-full ${i % 2 === 0 ? "bg-black" : "bg-gray-400"}`}
                />
              ))}
            </div>
            <span className="text-xl font-semibold tracking-tight text-black">
              Grokboard
            </span>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
          <Link href="/dashboard" className="text-black">
            Dashboard
          </Link>
          <Link href="#" className="hover:text-black transition-colors">
            Courses
          </Link>
          <Link href="#" className="hover:text-black transition-colors">
            Progress
          </Link>
          <Link href="#" className="hover:text-black transition-colors">
            Community
          </Link>
        </nav>

        {/* User Menu */}
        <Button variant="ghost" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm font-medium">
            {userName.charAt(0)}
          </div>
          <span className="text-sm font-medium text-gray-700">{userName} Chen</span>
          <ChevronDown className="w-4 h-4 text-gray-500" />
        </Button>
      </header>

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
              <path d="M40,80 Q60,40 100,60" fill="none" stroke="black" strokeWidth="2" />
              <path d="M150,30 L160,50" fill="none" stroke="black" strokeWidth="2" />
            </svg>
          </div>

          {/* Welcome Text */}
          <div className="flex-1">
            <h1 className="text-4xl font-semibold text-black mb-3">
              Welcome back, {userName}!
            </h1>
            <p className="text-gray-600 text-lg mb-6">
              Continue your learning journey today. You have <span className="font-semibold">{tasksDue} tasks due</span> this week.
            </p>

            {/* Progress Bar */}
            <div className="max-w-md">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm font-medium text-gray-700">Course Progress:</span>
                <span className="text-sm text-gray-600">{courseProgress}% complete</span>
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
            <p className="text-sm text-gray-600 mb-4">Loading modules...</p>
          )}
          {error && (
            <p className="text-sm text-red-600 mb-4">{error}</p>
          )}

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
