# 🎨 Stitch MCP — Full Skills Reference
**Project: LeadScout — Google Maps Lead Scraper**
*Saved: 2026-03-19 | Location: `c:\Users\MY PC\OneDrive\Desktop\google maps\`*

---

## 📌 What Is Stitch MCP?

Stitch MCP (Model Context Protocol) is a Google tool that lets AI assistants like Antigravity **generate, edit, and iterate on UI/UX design screens** using natural language prompts — without ever opening a design tool. Think of it as Figma, but controlled entirely by AI prompts.

Stitch output can be used as:
- Visual prototypes (screenshots)
- Design references for implementing React/Next.js/Vite UIs
- Component-level design specs with design tokens (fonts, colors, spacing)

---

## 🧰 Available Stitch MCP Tools (Full List)

| Tool | Purpose |
|------|---------|
| `create_project` | Create a new Stitch design project container |
| `generate_screen_from_text` | Generate a brand-new UI screen from a text prompt |
| `edit_screens` | Edit/refine existing screens using a new prompt |
| `generate_variants` | Create multiple design variations of an existing screen |
| `get_project` | Retrieve full metadata for a Stitch project |
| `get_screen` | Retrieve a single screen's details and screenshot URL |
| `list_projects` | List all your Stitch projects |
| `list_screens` | List all screens in a given project |

---

## 🔧 Tool-by-Tool Skills

---

### 1. `create_project` — Start a New Design Project

**When to use:** Start fresh for a new app, page, or design theme.

```
Tool: mcp_StitchMCP_create_project
Params:
  title: "LeadScout Dashboard Redesign"
```

**Skill Tips:**
- Always give a descriptive title — it acts as context for all screens inside.
- One project = one app/design system. Don't mix unrelated designs.
- Projects remember your design theme (dark/light mode, font, color accent, roundness).

---

### 2. `generate_screen_from_text` — Create a New Screen

**When to use:** Design a new page from scratch using a description.

```
Tool: mcp_StitchMCP_generate_screen_from_text
Params:
  projectId: "YOUR_PROJECT_ID"
  prompt: "A dark-themed lead scraper dashboard with a left panel for location/profession filters and a right panel showing a live data table of leads. Purple/violet accent colors. Premium glassmorphism card style."
  deviceType: "DESKTOP"   # or MOBILE / TABLET
```

**Skill Tips:**
- **Be extremely descriptive**: Include layout, color palette, typography feel, component types, and interaction hints.
- Mention the **exact pages/sections** you want: header, sidebar, cards, tables, modals, etc.
- Specify **device type** explicitly — desktop and mobile generate very different layouts.
- Use adjectives like: `glassmorphism`, `minimal`, `premium`, `brutalist`, `neomorphic`, `editorial`, `SaaS-style`, `dashboard`, `landing page`.
- Mention **data shown**: e.g., "show fake lead data rows with Name, Phone, Owner, Email, Website columns".
- Include **UI states**: active/hover/loading/empty states if needed.

**Example prompt for LeadScout:**
```
"A premium dark SaaS dashboard for a B2B lead scraper called LeadScout.
Left sidebar (380px): Country searchable dropdown, city selector, area chip tags,
profession pill buttons, a large purple 'Launch Scraper' CTA button.
Right panel: 4 stat cards (Total Leads, With Owner, With Email, With Website)
with large monospace numbers, a progress bar with percentage, and a live data table
with columns: Business, Phone, Owner, Email, Website, Dev Opportunity badge.
Color palette: Deep purple/void backgrounds (#08000f, #0d0118), accent violet (#a855f7),
accent pink (#e879f9). Font: Inter. Glassmorphism cards with subtle border glow."
```

---

### 3. `edit_screens` — Refine an Existing Screen

**When to use:** You've generated a screen but want to change specific parts.

```
Tool: mcp_StitchMCP_edit_screens
Params:
  projectId: "YOUR_PROJECT_ID"
  selectedScreenIds: ["SCREEN_ID_HERE"]
  prompt: "Change the primary accent color from blue to violet-purple. Make the navigation taller (72px). Add a glowing neon border to the stat cards."
```

**Skill Tips:**
- Be **surgical in your edits** — describe only what you want to change.
- You can request **component-level changes**: "change only the button style to pill-shaped with gradient fill".
- Use this for **iterative refinement**: generate first, then polish with multiple edits.
- You can edit **multiple screens at once** by passing multiple screen IDs — useful for global changes like updating nav or footer across all pages.
- Always get the `screenId` from `list_screens` first.

**Useful edit prompts:**
- `"Add a top navigation bar with LeadScout logo on the left, Sign Out button on the right"`
- `"Replace the table with a card grid layout for mobile view"`
- `"Add a loading skeleton state to the lead table"`
- `"Make the left panel sticky/fixed on scroll"`
- `"Add empty state illustration with message 'Configure and launch to collect leads'"`

---

### 4. `generate_variants` — Create Multiple Design Options

**When to use:** You want to explore multiple visual approaches before committing to one.

```
Tool: mcp_StitchMCP_generate_variants
Params:
  projectId: "YOUR_PROJECT_ID"
  selectedScreenIds: ["SCREEN_ID_HERE"]
  prompt: "Generate variants for the homepage hero section"
  variantOptions:
    count: 3
    creativeRange: "HIGH"       # LOW / MEDIUM / HIGH
    aspects: ["color", "layout", "typography"]
```

**Skill Tips:**
- Use `creativeRange: "HIGH"` when you want drastically different options.
- Use `creativeRange: "LOW"` for subtle polishing variations of the same design.
- Best used on **hero sections, landing pages, and marketing components** where visual variety matters most.
- After picking a variant, use `edit_screens` to finalize it.

---

### 5. `get_screen` — Retrieve Screen Details + Screenshot

**When to use:** After generating/editing, fetch the screenshot URL to view the result.

```
Tool: mcp_StitchMCP_get_screen
Params:
  name: "projects/PROJECT_ID/screens/SCREEN_ID"
  projectId: "PROJECT_ID"
  screenId: "SCREEN_ID"
```

**Returns:**
- A `downloadUrl` for the rendered screenshot image.
- Screen metadata (width, height, creation time).
- The generated HTML/CSS code (if available).

**Skill Tips:**
- Always call `get_screen` after `generate_screen_from_text` or `edit_screens` to confirm your output visually.
- The screenshot URL is a Google-hosted image — it can be embedded or previewed directly.
- Use the screenshot as a **design reference** for coding the component.

---

### 6. `list_screens` — View All Screens in a Project

**When to use:** Get all screen IDs before editing or generating variants.

```
Tool: mcp_StitchMCP_list_screens
Params:
  projectId: "PROJECT_ID"
```

**Returns:** All screens with their IDs, names, dimensions, and positions on the canvas.

---

### 7. `list_projects` — View All Your Stitch Projects

**When to use:** Find existing project IDs, check what designs are already made.

```
Tool: mcp_StitchMCP_list_projects
```

**Your Current Projects:**
| Title | Project ID | Device | Theme |
|-------|-----------|--------|-------|
| MST Artisan Bakery Website | `13163901388003829913` | Desktop | Light, Work Sans, Gold |
| UIU Calculator Redesign | `15726984557837730609` | Desktop | Dark, Inter, Blue |
| GradeFlow SaaS - Premium Minimalist | `6019704240060567774` | Desktop | Light, Plus Jakarta Sans, Blue |

---

## 🎯 LeadScout-Specific Design Prompts

Use these ready-made prompts to enhance the LeadScout UI with Stitch MCP:

### Homepage (Hero Section)
```
"Premium dark SaaS landing page for 'LeadScout' — a Google Maps lead scraper.
Hero section: centered layout, large headline 'Find every lead. Own every market.'
with violet gradient text. Subtitle text in muted purple. Two CTA buttons:
'Start Scraping →' (solid violet) and 'See Features' (ghost/outlined).
Below hero: a 4-column stat bar showing '140K+ Leads per profession', '50+ Countries',
'15+ Data points per lead', '100% Auto-enriched'. Background: deep void black (#08000f)
with animated sparkle particles. Font: Inter 800. Accent: violet-purple (#a855f7)."
```

### Dashboard / Scraper Panel
```
"Dark SaaS dashboard for LeadScout lead scraper. Two-column layout (380px left + flex right).
LEFT PANEL cards:
1. 'Target Location' card: searchable country dropdown, city selector, area chip tags
   with toggle on/off, an 'Add custom area' text input.
2. 'Profession/Niche' card: pill buttons for 30 professions (dentist, gym, lawyer etc),
   plus a custom profession text input.
3. Launch button: full-width solid violet gradient 'Launch Scraper →' CTA.
RIGHT PANEL:
4. 4 stat cards in a grid: Total Leads, With Owner, With Email, With Website.
   Large monospace numbers in violet/pink/purple accent colors.
5. Progress card with animated progress bar and percentage.
6. Live feed table: Business, Phone, Owner, Email, Website, Dev? columns.
   Rows animate in as they arrive. Empty state with centered icon.
Color: #08000f background, #160028 cards, #a855f7 accent, #c084fc violet, #e879f9 pink.
Font: Inter for UI, JetBrains Mono for data. Glassmorphism card borders."
```

### Login Page
```
"Centered dark authentication screen for 'LeadScout'. Logo at top.
A single glassmorphism card (420px wide) with:
- 'Welcome back' heading, subtitle text.
- Email input field, Password input field with clean purple focus ring.
- 'Sign in →' full-width button in solid violet.
- Divider line with 'or'.
- Toggle to switch between Sign In / Sign Up modes.
- Animated sparkle particle background.
- Error state: red-tinted error message box below inputs.
Color palette: deep void black background, card in #160028, inputs in #0f001e,
accent #a855f7. Font: Inter."
```

### Admin Panel
```
"Dark SaaS admin panel for LeadScout application.
Top navigation with logo, nav links (Dashboard, Profile, Admin), user name display, sign out button.
Main content area with:
- User management table: columns Name, Email, Role (admin/user badge), Created date, Actions.
- Pill badges: admin (violet), user (muted).
- Row action buttons: Edit (ghost), Delete (danger red).
- Empty state with centered icon.
- Stat cards at top: Total Users, Total Leads Scraped.
Dark background #08000f, card surface #160028, table rows with subtle separator lines."
```

### Profile Page
```
"Dark SaaS user profile page for LeadScout.
Avatar placeholder with initials, user name large heading, email below.
Stats section: number of scraping jobs, total leads collected, member since date.
Settings card below: change name input, save button.
Danger zone card: Sign out button and delete account (red danger styling).
Same dark purple color system as rest of app."
```

---

## 🚀 Full Workflow: Design → Code

Follow this end-to-end process to enhance LeadScout using Stitch MCP:

```
Step 1: CREATE PROJECT
  → mcp_StitchMCP_create_project({ title: "LeadScout UI Redesign" })
  → Save the returned project ID

Step 2: GENERATE SCREENS
  → For each page (Home, Login, Dashboard, Admin, Profile):
      mcp_StitchMCP_generate_screen_from_text({
        projectId: "...",
        prompt: "[use prompts from above]",
        deviceType: "DESKTOP"
      })
  → Also generate MOBILE variants of each screen

Step 3: VIEW & REVIEW
  → mcp_StitchMCP_list_screens({ projectId: "..." })
  → mcp_StitchMCP_get_screen({ ... }) for each screen
  → View the screenshot downloadUrl

Step 4: ITERATE WITH EDITS
  → mcp_StitchMCP_edit_screens({
      projectId: "...",
      selectedScreenIds: ["screen_id"],
      prompt: "specific change description"
    })

Step 5: GENERATE VARIANTS (if needed)
  → mcp_StitchMCP_generate_variants({
      projectId: "...",
      selectedScreenIds: ["screen_id"],
      prompt: "explore different layouts",
      variantOptions: { count: 2, creativeRange: "HIGH" }
    })

Step 6: CODE THE DESIGN
  → Extract design tokens (colors, fonts, spacing, borders)
  → Update App.css with new CSS variables
  → Rebuild React components to match Stitch screenshots
  → Ensure pixel-perfect fidelity
```

---

## 💎 Design Token Reference (Current LeadScout System)

These are the current design variables in `App.css`. Use them in prompts:

```css
/* Backgrounds */
--bg-void: #08000f;       /* page background */
--bg-deep: #0d0118;       /* secondary bg */
--bg-surface: #130024;    /* section bg */
--bg-card: #160028;       /* card bg */
--bg-card-hover: #1c0033; /* card hover */
--bg-input: #0f001e;      /* input bg */

/* Borders */
--border: rgba(147,51,234,0.15);  /* subtle purple border */

/* Accent Colors */
--accent-cyan: #a855f7;           /* primary accent (violet) */
--accent-violet: #c084fc;         /* secondary (light violet) */
--accent-gold: #e879f9;           /* tertiary (pink) */
--accent-green: #a78bfa;          /* positive/success */
--accent-red: #f87171;            /* error/danger */

/* Text */
--text-primary: #ffffff;
--text-secondary: #c4b5fd;
--text-muted: #7c3aed;

/* Typography */
--font-display: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Border Radius */
--radius-sm: 6px;
--radius-md: 10px;
--radius-lg: 16px;
```

---

## 📐 Component Inventory (LeadScout Current State)

| Component | File | Status |
|-----------|------|--------|
| Navigation Bar | `components/Nav.jsx` | ✅ Done |
| Sparkles Background | `components/SparklesBg.jsx` | ✅ Done |
| Home Page | `pages/HomePage.jsx` | ✅ Done |
| Login / Register | `pages/LoginPage.jsx` | ✅ Done |
| Dashboard (Scraper) | `pages/DashboardPage.jsx` | ✅ Done |
| Profile Page | `pages/ProfilePage.jsx` | ✅ Done |
| Admin Panel | `pages/AdminPage.jsx` | ✅ Done |
| Global CSS System | `App.css` | ✅ Done |
| Router Setup | `App.jsx` | ✅ Done |

**Areas to enhance with Stitch:**
- [ ] Mobile-responsive versions of all pages
- [ ] Enhanced hero animations on HomePage
- [ ] Better empty state illustrations on DashboardPage
- [ ] Richer stat cards with sparkline micro-charts
- [ ] Profile page avatar & settings section
- [ ] Modal dialogs for confirmations
- [ ] Onboarding/walkthrough overlay

---

## 🧠 Pro Tips for Using Stitch MCP

1. **Prompt length matters**: Longer, more descriptive prompts = better output. Don't be lazy.
2. **Reference existing screens**: Say "similar to the dashboard screen we made" to derive styles.
3. **Ask for specific states**: "Show the table in loading state with skeleton rows"
4. **Request annotations**: "Label each section clearly for developer handoff"
5. **Mobile-first**: Always generate a mobile variant — most users will be on phones.
6. **Iterate fast**: Generate → View → Edit is a 3-step loop. Don't try to perfect the first prompt.
7. **Color names work**: "Deep space navy", "neon electric violet", "warm amber gold" all work well.
8. **Be industry-specific**: Say "SaaS dashboard", "B2B tool", "developer tool" for appropriate aesthetics.
9. **Font counts**: Specify fonts like "Inter 800 for headings, Inter 400 for body" for consistency.
10. **Use modelId**: For best results, use `GEMINI_3_PRO` or `GEMINI_3_1_PRO` as the modelId.

---

## 📂 File Reference

```
c:\Users\MY PC\OneDrive\Desktop\google maps\
├── STITCH_MCP_SKILLS.md          ← YOU ARE HERE (this file)
├── leadscout\
│   ├── frontend\
│   │   └── src\
│   │       ├── App.jsx           ← Router + auth state
│   │       ├── App.css           ← Global design system
│   │       ├── main.jsx          ← Entry point
│   │       ├── components\
│   │       │   ├── Nav.jsx       ← Top navigation
│   │       │   └── SparklesBg.jsx ← Animated background
│   │       └── pages\
│   │           ├── HomePage.jsx  ← Landing page
│   │           ├── LoginPage.jsx ← Auth page
│   │           ├── DashboardPage.jsx ← Main scraper UI
│   │           ├── ProfilePage.jsx   ← User profile
│   │           └── AdminPage.jsx     ← Admin panel
│   └── backend\
│       └── main.py               ← FastAPI backend
├── scraper.py                    ← Core scraper logic
└── utils.py                      ← Enrichment utilities
```

---

*This file was auto-generated by Antigravity AI on 2026-03-19.*
*Use this as your playbook whenever working on LeadScout UI with Stitch MCP.*
