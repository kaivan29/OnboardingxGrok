import { ModuleStatus } from "@/components/dashboard/WeeklyModuleCard";

// ============================================================================
// Types
// ============================================================================

export type SubItem = {
  id: string; // Used as anchor hash for scroll (e.g., "#introduction")
  title: string;
};

export type Chapter = {
  id: string; // Used as route param for chapter page
  title: string;
  content: string; // Markdown string
  subItems?: SubItem[];
};

export type WeeklyTask = {
  id: string;
  title: string;
  description: string; // Shown in modal
  assignedBy: string;
  timeAgo: string;
  progress: number; // 0-100
};

export type WeekContent = {
  weekId: number;
  title: string;
  goal?: string; // Week goal from Grok curriculum
  status: ModuleStatus;
  overview: string; // Markdown string for week overview page
  chapters: Chapter[];
  tasks: WeeklyTask[];
};

// ============================================================================
// Mock Data
// ============================================================================

export const weekContents: WeekContent[] = [
  {
    weekId: 1,
    title: "Foundations & Setup",
    status: "completed",
    overview: `# Overview

This week's learning focuses on establishing a solid foundation with clear learning objectives, removing complexity, and building bases that provide context and supporting environments.

Key concepts are systematically presented with waves of responsibility, and comprehensive resources to effectively improve learning, and incorporate them into activities on access and overall engagements in your needs.

Expected outcomes include mastering complexity management principles: practical, continuous development and application in learning and practice investments.

## Key takeaways

- Learn the fundamentals of online learning as the core framework
- Revolve around style and transitioning to new concepts
- Determine where the applicable content is found in a secure executing environment
- Evaluate the complete process of the fully-learned concepts`,
    chapters: [
      {
        id: "how-to-learn",
        title: "How to Learn Effectively",
        content: `# How to Learn Effectively

Learning effectively requires understanding your own learning style and applying proven techniques consistently.

## Introduction

The foundation of effective learning lies in understanding how your brain processes and retains information. This chapter will guide you through evidence-based strategies.

## Active Recall

Active recall is the practice of stimulating your memory during the learning process. Instead of passively reading, you actively try to remember information.

### Benefits of Active Recall

- Strengthens neural pathways
- Identifies knowledge gaps early
- Improves long-term retention

## Spaced Repetition

Spaced repetition involves reviewing material at increasing intervals over time.

### Implementation Tips

- Start with short intervals (1 day)
- Gradually increase spacing
- Use flashcards or apps to track progress`,
        subItems: [
          { id: "introduction", title: "Introduction" },
          { id: "active-recall", title: "Active Recall" },
          { id: "spaced-repetition", title: "Spaced Repetition" },
        ],
      },
      {
        id: "creating-environment",
        title: "Creating Your Environment",
        content: `# Creating Your Learning Environment

A well-designed learning environment can significantly boost your productivity and focus.

## Workspace Setup

Your physical workspace should be optimized for focus and comfort.

### Essential Elements

- Good lighting (natural preferred)
- Ergonomic seating
- Minimal distractions
- Organized materials

## Digital Environment

Your digital tools should support, not hinder, your learning.

### Recommended Tools

- Note-taking apps with sync
- Focus timers (Pomodoro)
- Distraction blockers`,
        subItems: [
          { id: "workspace-setup", title: "Workspace Setup" },
          { id: "digital-environment", title: "Digital Environment" },
        ],
      },
    ],
    tasks: [
      {
        id: "task-1-1",
        title: "Refactor myFunction",
        description:
          "Review the myFunction implementation in the codebase and refactor it to improve readability and performance. Focus on breaking down complex logic into smaller, testable units.",
        assignedBy: "Bryan Ansong",
        timeAgo: "2 hrs ago",
        progress: 75,
      },
      {
        id: "task-1-2",
        title: "Complete Setup Quiz",
        description:
          "Complete the setup quiz to verify your understanding of the development environment configuration. This covers IDE setup, version control, and project structure.",
        assignedBy: "Bryan Ansong",
        timeAgo: "2 hrs ago",
        progress: 50,
      },
      {
        id: "task-1-3",
        title: "Environment Configuration",
        description:
          "Configure your local development environment according to the provided specifications. Ensure all dependencies are installed and the project builds successfully.",
        assignedBy: "Bryan Ansong",
        timeAgo: "2 hrs ago",
        progress: 100,
      },
    ],
  },
  {
    weekId: 2,
    title: "Data Structures",
    status: "continue",
    overview: `# Overview

This week dives deep into fundamental data structures that form the backbone of efficient programming.

You will learn about arrays, linked lists, stacks, queues, and trees. Understanding these structures is crucial for writing performant code.

## Key takeaways

- Understand time and space complexity
- Implement common data structures from scratch
- Choose the right data structure for different problems
- Analyze trade-offs between different approaches`,
    chapters: [
      {
        id: "arrays-lists",
        title: "Arrays and Lists",
        content: `# Arrays and Lists

Arrays and lists are the most fundamental data structures in programming.

## Arrays

Arrays store elements in contiguous memory locations.

### Characteristics

- Fixed size (in most languages)
- O(1) access by index
- O(n) insertion/deletion

## Linked Lists

Linked lists store elements with pointers to next elements.

### Characteristics

- Dynamic size
- O(n) access by index
- O(1) insertion/deletion at known position`,
        subItems: [
          { id: "arrays", title: "Arrays" },
          { id: "linked-lists", title: "Linked Lists" },
        ],
      },
      {
        id: "stacks-queues",
        title: "Stacks and Queues",
        content: `# Stacks and Queues

Stacks and queues are abstract data types with specific access patterns.

## Stacks

Last In, First Out (LIFO) data structure.

### Use Cases

- Function call stack
- Undo operations
- Expression parsing

## Queues

First In, First Out (FIFO) data structure.

### Use Cases

- Task scheduling
- BFS traversal
- Print queue`,
        subItems: [
          { id: "stacks", title: "Stacks" },
          { id: "queues", title: "Queues" },
        ],
      },
    ],
    tasks: [
      {
        id: "task-2-1",
        title: "Implement LinkedList",
        description:
          "Implement a doubly linked list with insert, delete, and search operations. Include proper edge case handling.",
        assignedBy: "Bryan Ansong",
        timeAgo: "1 day ago",
        progress: 25,
      },
      {
        id: "task-2-2",
        title: "Stack Practice",
        description:
          "Solve 3 stack-based problems from the practice set. Focus on understanding when to use stacks.",
        assignedBy: "Bryan Ansong",
        timeAgo: "1 day ago",
        progress: 0,
      },
    ],
  },
  {
    weekId: 3,
    title: "Algorithms",
    status: "start",
    overview: `# Overview

This week focuses on fundamental algorithms including sorting, searching, and graph algorithms.

## Key takeaways

- Master common sorting algorithms
- Understand search techniques
- Learn graph traversal methods
- Analyze algorithm efficiency`,
    chapters: [
      {
        id: "sorting",
        title: "Sorting Algorithms",
        content: `# Sorting Algorithms

Sorting is one of the most fundamental operations in computer science.

## Comparison Sorts

- Bubble Sort
- Merge Sort
- Quick Sort

## Non-Comparison Sorts

- Counting Sort
- Radix Sort`,
        subItems: [
          { id: "comparison-sorts", title: "Comparison Sorts" },
          { id: "non-comparison-sorts", title: "Non-Comparison Sorts" },
        ],
      },
    ],
    tasks: [
      {
        id: "task-3-1",
        title: "Implement QuickSort",
        description:
          "Implement the QuickSort algorithm with proper pivot selection and partition logic.",
        assignedBy: "Bryan Ansong",
        timeAgo: "3 days ago",
        progress: 0,
      },
    ],
  },
  {
    weekId: 4,
    title: "Summary",
    status: "locked",
    overview: `# Overview

This week consolidates all learnings from previous weeks.

## Key takeaways

- Review all concepts
- Complete final assessment
- Plan next steps`,
    chapters: [
      {
        id: "review",
        title: "Course Review",
        content: `# Course Review

A comprehensive review of all topics covered.`,
        subItems: [],
      },
    ],
    tasks: [],
  },
];

// ============================================================================
// Helper Functions
// ============================================================================

export function getWeekContent(weekId: number): WeekContent | undefined {
  return weekContents.find((w) => w.weekId === weekId);
}

export function getChapter(
  weekId: number,
  chapterId: string
): Chapter | undefined {
  const week = getWeekContent(weekId);
  return week?.chapters.find((c) => c.id === chapterId);
}

export function getAllWeeks(): Pick<
  WeekContent,
  "weekId" | "title" | "status"
>[] {
  return weekContents.map(({ weekId, title, status }) => ({
    weekId,
    title,
    status,
  }));
}
