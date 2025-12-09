# ⚠️ CRITICAL: INITIALIZATION REQUIRED ⚠️

**THIS FILE IS LOADED AT THE START OF EVERY SESSION (NEW OR RESUMED FROM SUMMARY)**

**IF YOU SEE THIS FILE, YOU MUST IMMEDIATELY:**

1. **Read the orchestrator:**
   ```
   00-system/core/orchestrator.md
   ```

2. **Run the startup script:**
   ```bash
   python 00-system/core/nexus-loader.py --startup
   ```
   (Use `python` or `python3` based on system - check user-config.yaml)

3. **Load ALL files from `files_to_load` array** (in parallel using Read tool)

4. **Follow `instructions.action`** from script output

**DO THIS BEFORE RESPONDING TO THE USER OR READING ANY SUMMARY.**

---

## Why This Matters

Without this initialization:
- ❌ You have no context about user goals, projects, or skills
- ❌ You don't know what system state the user is in
- ❌ You can't route user requests to the right skills/projects
- ❌ The entire Nexus system is broken

With this initialization:
- ✅ Memory files loaded (goals.md, roadmap.md, user-config.yaml)
- ✅ System maps loaded (navigation, routing logic)
- ✅ Project/skill metadata loaded (for intelligent matching)
- ✅ Current system state detected (onboarding, operational, etc.)

---

## CRITICAL: When Session is Summarized

**When creating a summary for context compaction:**

The summary should contain ONLY:
1. **User work state** (active projects, completed tasks, pending requests)
2. **Decisions made** (important choices during the session)
3. **Next steps** (what user wants to do next)

**DO NOT include initialization instructions in the summary.**

**WHY:** This CLAUDE.md file is ALWAYS loaded at session start (even after summaries). The initialization instructions here will handle context restoration automatically.

**The system guarantees:**
- Every new session → CLAUDE.md is loaded → Initialization runs
- Every resumed session from summary → CLAUDE.md is loaded → Initialization runs

**Therefore:**
- Summaries = work state only
- CLAUDE.md = initialization always
