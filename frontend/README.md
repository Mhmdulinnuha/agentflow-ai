# AgentFlow AI — Frontend

Frontend workspace for AgentFlow AI. Built with Next.js App Router, React, TypeScript, Tailwind CSS v4, Zustand, and Lucide icons.

## Architecture

```text
src/
├── app/                    # Next.js routes and global styles
├── components/
│   ├── layout/             # App shell, navigation, shared layouts
│   └── ui/                 # Reusable UI primitives
├── features/               # Feature-first modules
│   ├── dashboard/
│   ├── playground/
│   ├── agents/
│   ├── knowledge/
│   ├── mcp/
│   ├── workflows/
│   ├── executions/
│   └── settings/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── types/
├── hooks/                  # Cross-feature React hooks
├── lib/api/                # Shared FastAPI HTTP client
├── config/                 # Public runtime configuration
├── stores/                 # Global client state (Zustand)
└── types/                  # Shared TypeScript contracts
```

### Dependency rules

- `app/` composes feature pages; it should contain minimal business logic.
- `features/<name>/` owns feature-specific UI, hooks, API services, and types.
- `components/ui/` contains generic reusable components only.
- `lib/api/` is the single shared HTTP entry point to FastAPI.
- The browser must not connect directly to PostgreSQL, Ollama, vector storage, or MCP servers. Those are backend responsibilities.
- Never put API secrets in `NEXT_PUBLIC_*` variables. Only non-secret browser configuration belongs there.

## Run locally

Requirements: Node.js 20.9+.

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open http://localhost:3000.

Set `NEXT_PUBLIC_API_BASE_URL` to the FastAPI base URL. Current screens still use preview/mock data; the API client is the integration foundation and individual features must be wired to backend endpoints.

## Quality checks

```bash
npm run lint
npm run build
```

The starter has been structurally reorganized but should be validated in your local environment after installing dependencies.
