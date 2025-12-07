"use client";

import Link from "next/link";
import { ChevronDown } from "lucide-react";

import { Button } from "@/components/ui/button";

type DashboardHeaderProps = {
  userFullName: string;
};

export function DashboardHeader({ userFullName }: DashboardHeaderProps) {
  const userInitial = userFullName.charAt(0) || "?";

  return (
    <header className="flex h-14 w-full items-center justify-between border-b border-gray-200 px-6 lg:px-12 bg-white">
      <div className="flex items-center gap-3">
        <Link href="/" className="flex items-center gap-3">
          <div className="grid grid-cols-3 gap-1 w-6 h-6">
            {[...Array(9)].map((_, i) => (
              <div
                key={i}
                className={`w-1 h-1 rounded-full ${
                  i % 2 === 0 ? "bg-black" : "bg-gray-400"
                }`}
              />
            ))}
          </div>
          <span className="text-xl font-semibold tracking-tight text-black">
            Grokboard
          </span>
        </Link>
      </div>

      <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
        <Link href="/dashboard" className="text-black">
          Dashboard
        </Link>
        <Link href="/codebase" className="hover:text-black transition-colors">
          Codebase
        </Link>
      </nav>

      <Button variant="ghost" className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm font-medium">
          {userInitial}
        </div>
        <span className="text-sm font-medium text-gray-700">
          {userFullName}
        </span>
        <ChevronDown className="w-4 h-4 text-gray-500" />
      </Button>
    </header>
  );
}
