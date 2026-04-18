// Serverless function: query the wiki via Claude API
// Same pattern as Enthousiasmes/Journal Intime backends

const ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages";

export async function handler(event) {
  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: corsHeaders(), body: "" };
  }

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      headers: corsHeaders(),
      body: JSON.stringify({ error: "Method not allowed" }),
    };
  }

  try {
    const { question } = JSON.parse(event.body);

    if (!question || typeof question !== "string") {
      return {
        statusCode: 400,
        headers: corsHeaders(),
        body: JSON.stringify({ error: "Missing 'question' field" }),
      };
    }

    // Load wiki index and relevant pages
    // In production, this reads from a pre-built JSON index bundled at deploy time
    // For now, we pass the question directly and let Claude work with its context
    const wikiContext = await loadWikiContext();

    const response = await fetch(ANTHROPIC_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": process.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 2048,
        system: `You are a research assistant querying a personal knowledge wiki built from arXiv papers.

The wiki contains summaries, concept pages, method descriptions, and cross-references.
Answer the user's question using ONLY the wiki content provided below.
Cite wiki pages in your answer using [page-name] notation.
If the wiki doesn't contain enough information, say so clearly.

WIKI CONTENT:
${wikiContext}`,
        messages: [{ role: "user", content: question }],
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Anthropic API error:", errorText);
      return {
        statusCode: 502,
        headers: corsHeaders(),
        body: JSON.stringify({ error: "Failed to query Claude" }),
      };
    }

    const data = await response.json();
    const answer = data.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("\n");

    return {
      statusCode: 200,
      headers: corsHeaders(),
      body: JSON.stringify({
        answer,
        model: data.model,
        usage: data.usage,
      }),
    };
  } catch (error) {
    console.error("Query function error:", error);
    return {
      statusCode: 500,
      headers: corsHeaders(),
      body: JSON.stringify({ error: "Internal server error" }),
    };
  }
}

function corsHeaders() {
  return {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

async function loadWikiContext() {
  // TODO: At build time, scripts/export_mkdocs.py generates a wiki-index.json
  // containing the index.md + all page summaries (first 200 words each).
  // This function reads that bundled JSON.
  //
  // For now, return a placeholder that Claude Code will populate.
  try {
    const fs = await import("fs");
    const path = await import("path");
    const indexPath = path.join(__dirname, "wiki-index.json");
    if (fs.existsSync(indexPath)) {
      return fs.readFileSync(indexPath, "utf-8");
    }
  } catch {
    // Fallback
  }
  return "Wiki is being built. No content available yet.";
}
