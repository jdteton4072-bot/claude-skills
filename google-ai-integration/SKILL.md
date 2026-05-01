---
name: google-ai-integration
description: Connect Claude to Google AI tools — AI Studio (Vertex AI), Google Stitch (AI UI design via MCP), and Google Stitch's AI Canvas. Use this skill when the user wants to generate UI designs from text prompts, scaffold production code from Stitch designs, or use Claude alongside Google's AI ecosystem.
---

# Google AI Integration

Connect Claude to Google's AI tools: **AI Studio / Vertex AI**, **Google Stitch** (AI UI design), and **Stitch's AI Canvas**.

## What Each Tool Does

| Tool | What it is | How Claude connects |
|------|-----------|-------------------|
| **Google AI Studio / Vertex AI** | Google's platform for Gemini models; also hosts Claude via Vertex AI | Claude models available directly on Vertex AI |
| **Google Stitch** | AI UI design tool — text prompt → high-fidelity UI + code | MCP server (`stitch-mcp`) lets Claude read designs and generate code |
| **Stitch AI Canvas** | Infinite multi-screen design canvas inside Stitch | Accessed through the same Stitch MCP integration |

---

## 1. Google AI Studio & Vertex AI

Claude is available as a hosted model on **Google Cloud Vertex AI** — you can use it with your GCP credits.

### Setup

```bash
# Authenticate with Google Cloud
gcloud auth application-default login

# Configure Claude Code to use Vertex AI
export ANTHROPIC_VERTEX_PROJECT_ID="your-gcp-project-id"
export CLOUD_ML_REGION="us-east5"

claude --model claude-sonnet-4-6
```

### Use Claude Code on Vertex AI

```bash
# Install the Vertex AI provider
pip install anthropic[vertex]
```

```python
import anthropic

client = anthropic.AnthropicVertex(
    project_id="your-gcp-project-id",
    region="us-east5",
)

message = client.messages.create(
    model="claude-sonnet-4-6@20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from Vertex AI!"}],
)
print(message.content)
```

> **Note:** Google AI Studio itself is for Gemini models. To use Claude *alongside* AI Studio workflows, route through Vertex AI where both Claude and Gemini are available.

---

## 2. Google Stitch via MCP

[Google Stitch](https://stitch.withgoogle.com/) is a free AI design tool (powered by Gemini 2.5 Pro) that turns text prompts into high-fidelity UI designs and production-ready code. The `stitch-mcp` server lets Claude Code read your Stitch designs directly — no copy-paste.

### Setup

**Step 1: Install the MCP server**

```bash
npx @davideast/stitch-mcp setup
```

**Step 2: Add to Claude Code config**

```bash
claude mcp add stitch npx @davideast/stitch-mcp start
```

Or manually in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["@davideast/stitch-mcp", "start"]
    }
  }
}
```

**Step 3: Restart Claude Code**

```bash
exit
claude
```

### Try It

```
Fetch my Stitch project "dashboard-v2", extract the design system into DESIGN.md, 
then scaffold React + Tailwind components matching those exact design tokens.
```

```
Look at the "onboarding" flow in my Stitch project and convert the 3 screens 
into a Next.js app with routing between them.
```

### What Claude can do with Stitch

| Ask Claude... | What happens |
|---------------|-------------|
| "Read my Stitch design tokens" | Pulls color, typography, spacing into your codebase |
| "Scaffold components from the Stitch dashboard screen" | Generates React/Vue/Svelte components |
| "Convert all 5 Stitch screens to Next.js pages" | Builds a routed multi-page app |
| "Compare my code to the Stitch design and fix gaps" | Audits implementation fidelity |

---

## 3. Stitch AI Canvas

Stitch's AI Canvas is the infinite multi-screen workspace inside Stitch — updated March 2026 to support up to 5 interconnected screens, voice commands, and interactive prototyping.

The Canvas is accessed through the **same MCP integration** as Stitch. Once `stitch-mcp` is running, Claude can read multi-screen canvas layouts.

### Canvas Workflow

1. Open [stitch.withgoogle.com](https://stitch.withgoogle.com/) and describe your app flow
2. Stitch generates up to 5 interconnected screens with a consistent design system
3. Claude Code (via MCP) reads all screens and scaffolds the full app

```
Read all screens from my Stitch canvas project "ecommerce-flow" 
and build a complete React app with navigation between them.
```

---

## Stitch Limits (Free tier, 2026)

- **350 generations/month** (Standard mode)
- **50 generations/month** (Experimental mode)
- No credit card required — just a Google account

---

## Troubleshooting

- **MCP not connecting** → Run `claude mcp list` to verify `stitch` appears; try `npx @davideast/stitch-mcp start` manually first
- **Vertex auth error** → Re-run `gcloud auth application-default login`
- **Stitch design not found** → Make sure you're logged into the same Google account in your browser and in the MCP config

---

Sources:
- [Google Stitch](https://stitch.withgoogle.com/)
- [stitch-mcp on GitHub](https://github.com/davideast/stitch-mcp)
- [Claude on Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude)
- [Claude Code on Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai)
