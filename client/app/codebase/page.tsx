"use client";

import Link from "next/link";
import { ArrowLeft, Code2, FileCode, FolderTree } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function CodebasePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="flex h-14 w-full items-center justify-between border-b border-gray-200 px-6 lg:px-12 bg-white">
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="flex items-center gap-3">
            <div className="grid grid-cols-3 gap-1 w-6 h-6">
              {[...Array(9)].map((_, i) => (
                <div
                  key={i}
                  className={`w-1 h-1 rounded-full ${i % 2 === 0 ? "bg-black" : "bg-gray-400"
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
          <Link href="/dashboard" className="hover:text-black transition-colors">
            Dashboard
          </Link>
          <Link href="/codebase" className="text-black">
            Codebase
          </Link>
          <Link href="/chat" className="hover:text-black transition-colors">
            Chat
          </Link>
        </nav>

        <div className="w-8" /> {/* Spacer for alignment */}
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 lg:px-12 py-12">
        {/* Back Link */}
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-black transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>

        {/* Page Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-semibold text-black mb-3">
            Project Codebase
          </h1>
          <p className="text-gray-600 text-lg">
            Explore the complete codebase for your onboarding project. Browse files, review code, and understand the project structure.
          </p>
        </div>

        {/* Placeholder Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* File Explorer Card */}
          <div className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
              <FolderTree className="w-6 h-6 text-gray-700" />
            </div>
            <h3 className="text-lg font-semibold text-black mb-2">
              File Explorer
            </h3>
            <p className="text-gray-600 text-sm">
              Navigate through the project directory structure and explore all files.
            </p>
          </div>

          {/* Code Viewer Card */}
          <div className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
              <FileCode className="w-6 h-6 text-gray-700" />
            </div>
            <h3 className="text-lg font-semibold text-black mb-2">
              Code Viewer
            </h3>
            <p className="text-gray-600 text-sm">
              View and read source code with syntax highlighting and line numbers.
            </p>
          </div>

          {/* Documentation Card */}
          <div className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
              <Code2 className="w-6 h-6 text-gray-700" />
            </div>
            <h3 className="text-lg font-semibold text-black mb-2">
              Documentation
            </h3>
            <p className="text-gray-600 text-sm">
              Access project documentation, comments, and code explanations.
            </p>
          </div>
        </div>

        {/* Coming Soon Notice */}
        <div className="mt-12 bg-gray-100 border border-gray-200 rounded-xl p-8 text-center">
          <Code2 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-black mb-2">
            Full Codebase Explorer Coming Soon
          </h2>
          <p className="text-gray-600 max-w-md mx-auto">
            We&apos;re building a complete codebase exploration experience. Soon you&apos;ll be able to browse, search, and understand your entire project right here.
          </p>
        </div>
      </main>
    </div>
  );
}
