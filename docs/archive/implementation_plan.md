# Cross-Platform Aergia Studio Plan (Flash Drive Edition)

## Goal
Prepare the Aergia Studio codebase for transfer to a MacBook Pro via Flash Drive. This avoids internet exposure but requires manual file copying.

## User Decision
- **Method**: Physical Flash Drive (High Security).
- **Trade-off**: No automatic syncing. You must manually copy the folder back and forth to keep them updated.

## Proposed Changes

### 1. Mac Compatibility Scripts
Since you cannot run `.bat` files on macOS, we will create `.sh` (Shell) equivalents.

#### [NEW] [setup_mac.sh](file:///c:/Users/z143d/Aergia_Studio/setup_mac.sh)
- **Purpose**: One-click setup for the Mac.
- **Actions**:
  - Installs Python dependencies (`pip install -r requirements.txt`).
  - Checks for Homebrew/Python.

#### [NEW] [launch_studio.sh](file:///c:/Users/z143d/Aergia_Studio/launch_studio.sh)
- **Purpose**: Launch the dashboard on Mac.
- **Actions**:
  - Runs `python3 aergia_dashboard.py`.

### 2. Transfer Hygiene
Copying Windows system files or Python cache to a Mac can cause errors.

#### [NEW] [prepare_for_transfer.bat](file:///c:/Users/z143d/Aergia_Studio/prepare_for_transfer.bat)
- **Purpose**: Run this **before** copying to the flash drive.
- **Actions**:
  - Deletes all `__pycache__` folders (compiled Windows python code).
  - Deletes `.DS_Store` (Mac garbage) if present.
  - Deletes temporary logs.

#### [NEW] [.gitignore](file:///c:/Users/z143d/Aergia_Studio/.gitignore)
- **Purpose**: Still recommended to keep the folder clean and ready for Git if you decide to use it later.

## Verification Plan
1.  **Run Cleanup**: User runs `prepare_for_transfer.bat`.
2.  **Copy**: User copies folder to Flash Drive.
3.  **Mac Setup**: User plugs drive into Mac, copies folder, and runs `sh setup_mac.sh`.
