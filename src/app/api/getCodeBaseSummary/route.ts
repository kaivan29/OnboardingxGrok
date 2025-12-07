import { NextRequest, NextResponse } from "next/server";
import { PREPROCESSED_WIKIS } from "@/data/wiki";

export function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const codebaseUrl = searchParams.get("codebase_url");

  if (!codebaseUrl) {
    return NextResponse.json({ error: "missing codebase_url" }, { status: 400 });
  }

  const wiki = PREPROCESSED_WIKIS[codebaseUrl];

  if (!wiki) {
    return NextResponse.json({ error: "codebase not indexed" }, { status: 404 });
  }

  return NextResponse.json({ wiki });
}
