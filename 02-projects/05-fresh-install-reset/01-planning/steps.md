# Fresh Install Reset - Execution Steps

**Last Updated**: 2025-12-11

**IMPORTANT**: Execute phases in order. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Delete User-Created Projects

- [ ] `rm -rf 02-projects/01-optional-onboarding-system`
- [ ] `rm -rf 02-projects/02-notion-api-skills-suite`
- [ ] `rm -rf 02-projects/03-memory-loader-script`
- [ ] `rm -rf 02-projects/04-airtable-master-skill`
- [ ] Create `02-projects/README.md`:
```markdown
# Projects

This folder contains your **temporal work** - tasks with a beginning, middle, and end.

## Creating Projects

Say **"create project"** to start a new project with AI-guided planning.

## Structure

Each project follows this structure:
{ID}-{project-name}/
├── 01-planning/     # overview.md, plan.md, steps.md
├── 02-resources/    # Reference materials
├── 03-working/      # Work in progress
└── 04-outputs/      # Final deliverables

## Projects vs Skills

- **Projects** = One-time work (finite deliverable)
- **Skills** = Reusable workflows (repeatable process)
```

---

## Phase 2: Delete Legacy Onboarding Projects

- [ ] `rm -rf 02-projects/00-onboarding`
- [ ] Verify learning skills exist: `ls 00-system/skills/learning/`
  - Should see: setup-goals, setup-workspace, learn-projects, learn-skills, learn-nexus

---

## Phase 3: Delete ALL Memory Files

- [ ] `rm -rf 01-memory/*`
- [ ] Verify folder is empty but exists: `ls 01-memory/`

**Note**: Memory files auto-regenerate on first `--startup` via SMART_DEFAULT_* templates in nexus-loader.py

---

## Phase 4: Clear User Skills Folder

- [ ] `rm -rf 03-skills/*`
- [ ] Create `03-skills/README.md`:
```markdown
# User Skills

This folder is for your **custom skills** - reusable workflows you create.

## Creating Skills

Say **"create skill"** to build a new skill from a workflow you repeat.

## How It Works

- User skills here take **priority** over system skills in `00-system/skills/`
- Each skill has a `SKILL.md` file with YAML metadata + workflow instructions

## Projects vs Skills

- **Projects** = One-time work (finite deliverable)
- **Skills** = Reusable workflows (repeatable process)
```

---

## Phase 5: Clear Workspace Folder

- [ ] `rm -rf 04-workspace/*`
- [ ] Create `04-workspace/README.md`:
```markdown
# Workspace

This folder is for your **working files** - documents, data, and outputs.

## Setting Up

Say **"setup workspace"** to organize this folder based on your work needs.

## Structure

You can organize however you like. Common structures:

04-workspace/
├── input/       # Files to process
├── output/      # Generated results
├── reference/   # Background materials
└── archive/     # Completed work
```

---

## Phase 6: Delete Dev/Test Artifacts

**Core tests & utilities**:
- [ ] `rm -rf 00-system/core/tests`
- [ ] `rm -f 00-system/core/count-tasks.py`
- [ ] `rm -f 00-system/core/uncheck-tasks.py`

**Skill test folders**:
- [ ] `rm -rf 00-system/skills/notion/airtable-master/tests`
- [ ] `rm -rf 00-system/skills/notion/notion-master/tests`
- [ ] `rm -rf 00-system/skills/projects/create-project/tests`
- [ ] `rm -rf 00-system/skills/system/close-session/tests`

**Example placeholder files** (find and delete all):
- [ ] `find 00-system/skills -name "example_asset.txt" -delete`
- [ ] `find 00-system/skills -name "example.py" -delete`

**Cache folders**:
- [ ] `rm -rf .pytest_cache`

---

## Phase 7: Delete Internal Documentation Projects

- [ ] `rm -rf 00-system/documentation/06-documentation-update-system-enhancements`
- [ ] `rm -rf 00-system/documentation/07-nexus-product-intro-presentation`
- [ ] `rm -rf 00-system/documentation/archive`
- [ ] `rm -rf 00-system/documentation/presentation-materials` (if exists)

---

## Phase 8: Delete Claude Local Settings

- [ ] `rm -rf .claude`

---

## Phase 9: Review init-memory.py

- [ ] Check if init-memory.py is referenced anywhere:
  - `grep -r "init-memory" 00-system/`
  - `grep -r "init_memory" 00-system/`
- [ ] If only referenced by deleted onboarding → DELETE: `rm -f 00-system/core/init-memory.py`
- [ ] If still needed → KEEP

---

## Phase 10: Final Verification

- [ ] Run: `python 00-system/core/nexus-loader.py --startup`
- [ ] Verify memory files auto-created in 01-memory/:
  - goals.md
  - user-config.yaml
  - core-learnings.md
  - memory-map.md
- [ ] Verify clean menu shows:
  - "Empty ▸ say 'setup goals' to teach me about you"
  - "None yet ▸ say 'create project' to start something"
- [ ] Verify no sensitive data remains:
  - `grep -r "api_key" . --include="*.md" --include="*.yaml"`
  - `grep -r "secret" . --include="*.md" --include="*.yaml"`
- [ ] Test "setup goals" skill works

---

## Phase 11: Cleanup (LAST STEP)

- [ ] `rm -rf 02-projects/05-fresh-install-reset`

---

## Summary Checklist

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Delete user projects (01-04) | [ ] |
| 2 | Delete legacy onboarding | [ ] |
| 3 | Delete memory files | [ ] |
| 4 | Clear user skills folder | [ ] |
| 5 | Clear workspace folder | [ ] |
| 6 | Delete dev/test artifacts | [ ] |
| 7 | Delete internal doc projects | [ ] |
| 8 | Delete .claude/ | [ ] |
| 9 | Review init-memory.py | [ ] |
| 10 | Final verification | [ ] |
| 11 | Delete this project | [ ] |

---

## Post-Reset State

**Empty folders with READMEs**:
- `01-memory/` (auto-populates on startup)
- `02-projects/README.md`
- `03-skills/README.md`
- `04-workspace/README.md`

**Preserved system**:
- `00-system/` (core, skills, documentation, mental-models)
- Root files (CLAUDE.md, GEMINI.md, README.md, .gitignore)

**Gitignored** (user creates own):
- `.env`
- `.mcp.json`
