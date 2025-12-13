# Implementation Steps

## Phase 1: Complete nexus-loader.py Integration

- [x] **1.1** Connect --check-update to check_for_updates() in main()
- [x] **1.2** Connect --sync to sync_from_upstream() in main()
- [x] **1.3** Handle --dry-run and --force flags in sync execution
- [x] **1.4** Test --check-update returns correct JSON
- [x] **1.5** Test --sync performs backup and checkout correctly

## Phase 2: Create update-nexus Skill

- [x] **2.1** Create skill folder: `00-system/skills/system/update-nexus/`
- [x] **2.2** Create SKILL.md with:
  - [x] YAML frontmatter (name, description with triggers)
  - [x] Purpose section
  - [x] Workflow steps
- [x] **2.3** Workflow Step 1: Check for updates
  - [x] Run `nexus-loader.py --check-update`
  - [x] Parse JSON response
  - [x] If no updates: display "Already up-to-date" and exit
- [x] **2.4** Workflow Step 2: Show what will change
  - [x] Display current version vs upstream version
  - [x] List files that will be updated
  - [x] Show protected folders reminder
- [x] **2.5** Workflow Step 3: Confirm with user
  - [x] Ask "Proceed with update? (yes/no)"
  - [x] If no: exit gracefully
- [x] **2.6** Workflow Step 4: Perform sync
  - [x] Run `nexus-loader.py --sync --force`
  - [x] Parse JSON response
  - [x] Handle errors gracefully
- [x] **2.7** Workflow Step 5: Display results
  - [x] Show success message with version change
  - [x] Show backup location
  - [x] Suggest: `git add . && git commit -m "Update Nexus to vX.X"`

## Phase 3: Startup Update Check (Optional)

- [x] **3.1** Add `--skip-update-check` flag to --startup
- [x] **3.2** In load_startup(), optionally call check_for_updates()
- [x] **3.3** Add `update_available` to stats output
- [x] **3.4** Add `update_info` object with version details
- [x] **3.5** Make update check non-blocking (don't fail startup on network error)

## Phase 4: Menu Update Notice

- [x] **4.1** Update orchestrator.md menu template
- [x] **4.2** Add conditional section for update notice:
  ```
  [If stats.update_available=true:]
  ⚡ UPDATE AVAILABLE: v{local} → v{upstream}
     Say 'update nexus' to get latest improvements
  ```
- [x] **4.3** Position notice prominently (after banner, before MEMORY)

## Phase 5: Documentation

- [x] **5.1** Update README.md with "Getting Nexus" section:
  - [x] "Use this template" instructions
  - [x] Clone instructions
  - [x] First run explanation
- [x] **5.2** Update README.md with "Getting Updates" section:
  - [x] Explain "update nexus" command
  - [x] Explain what syncs vs what's protected
  - [x] Explain backup system
- [x] **5.3** Create CHANGELOG.md in 00-system/:
  - [x] Document v0.82.0 changes
  - [x] Establish format for future versions

## Phase 6: GitHub Template Setup

- [ ] **6.1** Mark repo as Template Repository (Settings → General)
- [x] **6.2** Verify all folders exist with starter content:
  - [x] 01-memory/ has template files
  - [x] 02-projects/ exists (with README)
  - [x] 03-skills/ exists (with README)
  - [x] 04-workspace/ has workspace-map.md
- [ ] **6.3** Test "Use this template" flow end-to-end

## Phase 7: Testing

- [ ] **7.1** Test: Fresh clone, first --check-update (adds upstream remote) [needs real upstream]
- [ ] **7.2** Test: --sync with no changes (already up-to-date) [needs real upstream]
- [ ] **7.3** Test: --sync with changes (backup created, files updated) [needs real upstream]
- [x] **7.4** Test: --sync with uncommitted changes (error message) ✓
- [x] **7.5** Test: --sync --force with uncommitted changes (proceeds) ✓
- [x] **7.6** Test: --sync --dry-run (shows changes, doesn't apply) ✓
- [x] **7.7** Test: Network failure handling ✓
- [ ] **7.8** Test: update-nexus skill full workflow [needs real upstream]
- [x] **7.9** Test: Menu shows update notice correctly ✓
