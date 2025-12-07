"use client";

import { SubItem } from "@/lib/data/week-content";

interface WeekContentAreaProps {
  title: string;
  content: string; // Markdown string
  subItems?: SubItem[];
}

export function WeekContentArea({
  title,
  content,
  subItems,
}: WeekContentAreaProps) {
  // Parse markdown content into sections
  const sections = parseMarkdownToSections(content, subItems);

  return (
    <article className="max-w-3xl">
      <h1 className="text-4xl font-bold text-black mb-8">{title}</h1>

      <div className="prose prose-gray max-w-none">
        {sections.map((section, index) => (
          <Section key={index} section={section} />
        ))}
      </div>
    </article>
  );
}

// ============================================================================
// Section Component
// ============================================================================

interface SectionData {
  id?: string;
  content: string;
}

function Section({ section }: { section: SectionData }) {
  return (
    <div id={section.id} className="scroll-mt-8">
      <MarkdownContent content={section.content} />
    </div>
  );
}

// ============================================================================
// Markdown Content Renderer
// ============================================================================

function MarkdownContent({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: React.ReactNode[] = [];
  let currentList: string[] = [];
  let listKey = 0;

  const flushList = () => {
    if (currentList.length > 0) {
      elements.push(
        <ul key={`list-${listKey++}`} className="list-disc pl-6 mb-4 space-y-2">
          {currentList.map((item, i) => (
            <li key={i} className="text-gray-700">
              {item}
            </li>
          ))}
        </ul>
      );
      currentList = [];
    }
  };

  lines.forEach((line, index) => {
    const trimmedLine = line.trim();

    // Skip the main title (# Title) as we display it separately
    if (trimmedLine.startsWith("# ") && index === 0) {
      return;
    }

    // H2 heading
    if (trimmedLine.startsWith("## ")) {
      flushList();
      elements.push(
        <h2
          key={`h2-${index}`}
          className="text-2xl font-semibold text-black mt-8 mb-4"
        >
          {trimmedLine.slice(3)}
        </h2>
      );
      return;
    }

    // H3 heading
    if (trimmedLine.startsWith("### ")) {
      flushList();
      elements.push(
        <h3
          key={`h3-${index}`}
          className="text-xl font-medium text-black mt-6 mb-3"
        >
          {trimmedLine.slice(4)}
        </h3>
      );
      return;
    }

    // List item
    if (trimmedLine.startsWith("- ")) {
      currentList.push(trimmedLine.slice(2));
      return;
    }

    // Empty line
    if (trimmedLine === "") {
      flushList();
      return;
    }

    // Regular paragraph
    flushList();
    elements.push(
      <p key={`p-${index}`} className="text-gray-700 mb-4 leading-relaxed">
        {trimmedLine}
      </p>
    );
  });

  // Flush any remaining list items
  flushList();

  return <>{elements}</>;
}

// ============================================================================
// Helper Functions
// ============================================================================

function parseMarkdownToSections(
  content: string,
  subItems?: SubItem[]
): SectionData[] {
  if (!subItems || subItems.length === 0) {
    return [{ content }];
  }

  // For now, return the whole content as a single section
  // A more sophisticated parser could split by subItem anchors
  const sections: SectionData[] = [];
  const lines = content.split("\n");
  let currentSection: SectionData = { content: "" };
  let currentLines: string[] = [];

  for (const line of lines) {
    const trimmedLine = line.trim();

    // Check if this is a heading that matches a subItem
    if (trimmedLine.startsWith("## ") || trimmedLine.startsWith("### ")) {
      const headingText = trimmedLine.replace(/^#{2,3}\s+/, "").toLowerCase();
      const matchingSubItem = subItems.find(
        (item) =>
          item.title.toLowerCase() === headingText ||
          item.id === headingText.replace(/\s+/g, "-")
      );

      if (matchingSubItem) {
        // Save current section if it has content
        if (currentLines.length > 0) {
          currentSection.content = currentLines.join("\n");
          sections.push(currentSection);
        }
        // Start new section
        currentSection = { id: matchingSubItem.id, content: "" };
        currentLines = [line];
        continue;
      }
    }

    currentLines.push(line);
  }

  // Add the last section
  if (currentLines.length > 0) {
    currentSection.content = currentLines.join("\n");
    sections.push(currentSection);
  }

  return sections.length > 0 ? sections : [{ content }];
}
