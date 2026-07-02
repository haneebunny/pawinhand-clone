import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  try {
    // Resolving data/Map_of_South_Korea.svg path relative to execution cwd
    const filePath = path.resolve(process.cwd(), "../data/Map_of_South_Korea.svg");
    
    if (!fs.existsSync(filePath)) {
      // Try fallback for different cwd structures
      const alternatePath = path.resolve(process.cwd(), "data/Map_of_South_Korea.svg");
      if (fs.existsSync(alternatePath)) {
        const svgContent = fs.readFileSync(alternatePath, "utf8");
        return new NextResponse(svgContent, {
          headers: { "Content-Type": "image/svg+xml" },
        });
      }
      return NextResponse.json({ error: `SVG file not found at ${filePath}` }, { status: 404 });
    }

    const svgContent = fs.readFileSync(filePath, "utf8");
    return new NextResponse(svgContent, {
      headers: {
        "Content-Type": "image/svg+xml",
      },
    });
  } catch (error) {
    console.error("Failed to serve map SVG", error);
    return NextResponse.json({ error: "Failed to read SVG file" }, { status: 500 });
  }
}
