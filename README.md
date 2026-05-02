# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Abhyas Kranti — AI Learning Hub (Added 2026-03-29)

- **Route**: `/ai-hub` (integrated into the main Abhyas Kranti portal)
- **Backend**: `artifacts/api-server/src/routes/ai.ts` — POST `/api/ai/claude` proxies to Anthropic Claude via Replit AI Integrations
- **Frontend**: `artifacts/abhyas-kranti/src/pages/AIHub.tsx` — 5-tab UI (Dashboard, Doubt Solver, PDF Quiz, SSB Psychology, DB Schema)
- **Supabase**: Client at `artifacts/abhyas-kranti/src/lib/supabase.ts`; Schema SQL at `SUPABASE_SCHEMA` const; tables prefixed `ak_`
- **AI utility**: `artifacts/abhyas-kranti/src/lib/aiHub.ts` — calls `/api/ai/claude`
- **Env vars**: `VITE_SUPABASE_URL` (shared), `VITE_SUPABASE_ANON_KEY` (secret), `AI_INTEGRATIONS_ANTHROPIC_*` (auto-set)
- **Link**: Footer of ExamHub has `⚡ AI Learning Hub` link

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Structure

```text
artifacts-monorepo/
├── artifacts/              # Deployable applications
│   └── api-server/         # Express API server
├── lib/                    # Shared libraries
│   ├── api-spec/           # OpenAPI spec + Orval codegen config
│   ├── api-client-react/   # Generated React Query hooks
│   ├── api-zod/            # Generated Zod schemas from OpenAPI
│   └── db/                 # Drizzle ORM schema + DB connection
├── scripts/                # Utility scripts (single workspace package)
│   └── src/                # Individual .ts scripts, run via `pnpm --filter @workspace/scripts run <script>`
├── pnpm-workspace.yaml     # pnpm workspace (artifacts/*, lib/*, lib/integrations/*, scripts)
├── tsconfig.base.json      # Shared TS options (composite, bundler resolution, es2022)
├── tsconfig.json           # Root TS project references
└── package.json            # Root package with hoisted devDeps
```

## TypeScript & Composite Projects

Every package extends `tsconfig.base.json` which sets `composite: true`. The root `tsconfig.json` lists all packages as project references. This means:

- **Always typecheck from the root** — run `pnpm run typecheck` (which runs `tsc --build --emitDeclarationOnly`). This builds the full dependency graph so that cross-package imports resolve correctly. Running `tsc` inside a single package will fail if its dependencies haven't been built yet.
- **`emitDeclarationOnly`** — we only emit `.d.ts` files during typecheck; actual JS bundling is handled by esbuild/tsx/vite...etc, not `tsc`.
- **Project references** — when package A depends on package B, A's `tsconfig.json` must list B in its `references` array. `tsc --build` uses this to determine build order and skip up-to-date packages.

## Root Scripts

- `pnpm run build` — runs `typecheck` first, then recursively runs `build` in all packages that define it
- `pnpm run typecheck` — runs `tsc --build --emitDeclarationOnly` using project references

## Packages

### `artifacts/api-server` (`@workspace/api-server`)

Express 5 API server. Routes live in `src/routes/` and use `@workspace/api-zod` for request and response validation and `@workspace/db` for persistence.

- Entry: `src/index.ts` — reads `PORT`, starts Express
- App setup: `src/app.ts` — mounts CORS, JSON/urlencoded parsing, routes at `/api`
- Routes: `src/routes/index.ts` mounts sub-routers; `src/routes/health.ts` exposes `GET /health` (full path: `/api/health`)
- Depends on: `@workspace/db`, `@workspace/api-zod`
- `pnpm --filter @workspace/api-server run dev` — run the dev server
- `pnpm --filter @workspace/api-server run build` — production esbuild bundle (`dist/index.cjs`)
- Build bundles an allowlist of deps (express, cors, pg, drizzle-orm, zod, etc.) and externalizes the rest

### `lib/db` (`@workspace/db`)

Database layer using Drizzle ORM with PostgreSQL. Exports a Drizzle client instance and schema models.

- `src/index.ts` — creates a `Pool` + Drizzle instance, exports schema
- `src/schema/index.ts` — barrel re-export of all models
- `src/schema/<modelname>.ts` — table definitions with `drizzle-zod` insert schemas (no models definitions exist right now)
- `drizzle.config.ts` — Drizzle Kit config (requires `DATABASE_URL`, automatically provided by Replit)
- Exports: `.` (pool, db, schema), `./schema` (schema only)

Production migrations are handled by Replit when publishing. In development, we just use `pnpm --filter @workspace/db run push`, and we fallback to `pnpm --filter @workspace/db run push-force`.

### `lib/api-spec` (`@workspace/api-spec`)

Owns the OpenAPI 3.1 spec (`openapi.yaml`) and the Orval config (`orval.config.ts`). Running codegen produces output into two sibling packages:

1. `lib/api-client-react/src/generated/` — React Query hooks + fetch client
2. `lib/api-zod/src/generated/` — Zod schemas

Run codegen: `pnpm --filter @workspace/api-spec run codegen`

### `lib/api-zod` (`@workspace/api-zod`)

Generated Zod schemas from the OpenAPI spec (e.g. `HealthCheckResponse`). Used by `api-server` for response validation.

### `lib/api-client-react` (`@workspace/api-client-react`)

Generated React Query hooks and fetch client from the OpenAPI spec (e.g. `useHealthCheck`, `healthCheck`).

### `artifacts/abhyas-kranti` (`@workspace/abhyas-kranti`)

React + Vite PWA — **Abhyas Kranti** — Universal Career & Education Portal. Navy Blue `#0a1628` + Gold `#D4AF37` theme.

**Owner**: Dr. Dnyaneshwar Gawalikar (`dsg150379@gmail.com`)
**Contact**: WhatsApp placeholder — set `WHATSAPP_NUMBER` const in `ExamHub.tsx`
**Route**: `/` (root artifact)

**Key files**:
- `src/pages/ExamHub.tsx` — main shell, NAV_TABS, footer, HeroSection integration
- `src/components/HeroSection.tsx` — animated hero with counters + CTA buttons
- `src/components/QuizSection.tsx` — MCQ quiz engine (5 categories, 10 Q each, timer)
- `src/components/TestimonialsSection.tsx` — 6 student testimonials + stats
- `src/components/HigherSection.tsx` — NEET/JEE/CET, Teachers, Research Hub
- `src/components/CurrentAffairsHub.tsx` — news portals, AIR, DD, magazines
- `src/components/WeeklyQuiz.tsx` — Google Form weekly quiz
- `src/components/SplashScreen.tsx` — sessionStorage key `abhyas-kranti-splash-shown`
- `src/pages/PrivacyPolicy.tsx` — bilingual Disclaimer & Privacy Policy (`/privacy`)

**Nav Tabs**: mentor | quiz | school | higher | admin | defense | banking | abroad | currentaffairs

**Important rules**:
- Never use `<a href="#">` — use disabled `<button>` for placeholders
- `Link` from wouter renders as `<a>` — do NOT nest another `<a>` inside it
- All external links: `target="_blank" rel="noopener noreferrer"`
- e-Balbharati: `cart.ebalbharati.in` (not `ebalbharati.in`)
- NTA mock tests: `abhyas.nta.ac.in`

### `scripts` (`@workspace/scripts`)

Utility scripts package. Each script is a `.ts` file in `src/` with a corresponding npm script in `package.json`. Run scripts via `pnpm --filter @workspace/scripts run <script>`. Scripts can import any workspace package (e.g., `@workspace/db`) by adding it as a dependency in `scripts/package.json`.
