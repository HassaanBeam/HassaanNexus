# Fresh Install Reset - Plan

**Last Updated**: 2025-12-11

---

## Approach

Systematic cleanup of Nexus-v4 in 10 phases, working from user content → dev artifacts → verification. Each phase is atomic and can be verified independently.

**Strategy**: Delete everything that's user-specific or development-related, while preserving:
- Core system (`00-system/`)
- Root configuration files (CLAUDE.md, README.md, .gitignore)
- Empty folder structure with explanatory READMEs

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Memory files** | DELETE all | nexus-loader.py has `SMART_DEFAULT_*` templates - auto-regenerates on startup |
| **Old onboarding (00-onboarding)** | DELETE | Superseded by learning skills in `00-system/skills/learning/` |
| **.env file** | KEEP (gitignored) | Already in .gitignore, users maintain their own |
| **.mcp.json** | KEEP (now gitignored) | Added to .gitignore - users create their own |
| **init-memory.py** | REVIEW | May be redundant since nexus-loader handles template creation |
| **Test files** | DELETE all | Development artifacts, not needed for distribution |
| **Internal doc projects (06, 07)** | DELETE | Project management folders, not system documentation |

---

## Resources Needed

**Tools/Access**:
- Bash/shell access for rm -rf commands
- Python for verification script

**Information Already Gathered**:
- Full codebase exploration completed
- SMART_DEFAULT_* templates confirmed in nexus-loader.py (lines 42-175)
- .gitignore already includes .env (line 31)
- .mcp.json added to .gitignore (line 52)

---

## Dependencies & Links

**Files to DELETE**:

| Category | Paths |
|----------|-------|
| User projects | `02-projects/01-*`, `02-projects/02-*`, `02-projects/03-*`, `02-projects/04-*` |
| Legacy onboarding | `02-projects/00-onboarding/` |
| Memory files | `01-memory/*` (all contents) |
| Integration caches | `01-memory/integrations/` |
| User skills | `03-skills/*` (all contents) |
| Workspace | `04-workspace/*` (all contents) |
| Core tests | `00-system/core/tests/` |
| Core utilities | `00-system/core/count-tasks.py`, `00-system/core/uncheck-tasks.py` |
| Skill tests | `00-system/skills/*/tests/` (all test folders) |
| Example files | `00-system/skills/learning/*/assets/example_asset.txt` |
| Example scripts | `00-system/skills/learning/*/scripts/example.py` |
| Internal docs | `00-system/documentation/06-*`, `00-system/documentation/07-*` |
| Doc archive | `00-system/documentation/archive/` |
| Presentation | `00-system/documentation/presentation-materials/` |
| Claude settings | `.claude/` |
| Pytest cache | `.pytest_cache/` |

**Files to CREATE**:

| Path | Purpose |
|------|---------|
| `02-projects/README.md` | Explain projects folder |
| `03-skills/README.md` | Explain user skills folder |
| `04-workspace/README.md` | Explain workspace folder |

**Files to KEEP**:

| Category | Items |
|----------|-------|
| Root | CLAUDE.md, GEMINI.md, README.md, .gitignore |
| Core system | `00-system/core/orchestrator.md`, `nexus-loader.py`, `validate-initialization.py`, `bulk-complete-onboarding.py` |
| System skills | All in `00-system/skills/` (except tests) |
| Documentation | Root docs in `00-system/documentation/` (product-overview.md, framework-overview.md, etc.) |
| Mental models | `00-system/mental-models/` |

---

## Current State Analysis

**Existing State**:
- 5 user projects (01-04 + this one)
- 4 legacy onboarding projects in 00-onboarding/
- Memory files with personalized content
- ~3000 lines of Airtable cache in integrations/
- Test folders scattered throughout skills
- Internal project folders (06, 07) in documentation

**Pain Points**:
- User-specific data would confuse new users
- Test files bloat distribution size
- Internal project folders look like system docs
- Legacy onboarding conflicts with new learning skills

---

## Process Design

**New Process Flow (Fresh Install Experience)**:

1. User clones/downloads Nexus-v4
2. User runs `python 00-system/core/nexus-loader.py --startup`
3. nexus-loader creates memory files from SMART_DEFAULT_* templates
4. User sees clean menu:
   - "Empty ▸ say 'setup goals' to teach me about you"
   - "None yet ▸ say 'create project' to start something"
5. User personalizes via learning skills (setup-goals, etc.)

**Improvements Expected**:
- Clean starting point (no confusion from existing projects)
- Smaller distribution size (~1.3MB vs ~2.7MB)
- Clear separation of system vs user content

---

## Mental Models Applied

**First Principles**:
- Q: What's the minimum needed for a functional fresh install?
- A: Core system + empty user folders + auto-regenerating memory templates

**Pre-Mortem**:
- Risk: Accidentally delete system files → Mitigation: Explicit DELETE list, backup exists
- Risk: Miss some user data → Mitigation: Comprehensive exploration already done
- Risk: Break startup flow → Mitigation: Verify with --startup after reset

**Checklist**:
- [x] What auto-regenerates? → Memory files via SMART_DEFAULT_*
- [x] What's already gitignored? → .env, .mcp.json (now)
- [x] What replaces old onboarding? → Learning skills
- [x] What's needed for new user? → Empty folders + README explanations

---

*Next: See steps.md for execution checklist*
