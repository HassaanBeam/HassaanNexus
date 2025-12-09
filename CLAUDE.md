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