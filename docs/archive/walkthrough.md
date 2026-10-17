# Moving Aergia to macOS (Flash Drive Method)

I have prepared your project for safe transfer and **fixed usage of hardcoded Windows paths** so it actually runs on Mac.

## 1. On Windows (Right Now)
1.  Double-click `prepare_for_transfer.bat` in your Aergia Studio folder.
    -   *This deletes junk files so the transfer is clean.*
2.  Copy the entire `Aergia_Studio` folder to your Flash Drive.

## 2. On Your Mac
1.  Copy the folder from the Flash Drive to your Mac (e.g., to `Documents`).
2.  Open **Terminal**.
3.  Type `cd ` (drag the folder into the terminal window) and press Enter.
4.  Run the setup script *once*:
    ```bash
    sh setup_mac.sh
    ```
5.  To launch the studio:
    ```bash
    sh launch_studio.sh
    ```

## 3. Code Modifications (Done)
I scanned your code and found many files essentially saying "Look in C:\Users\z143d...". **This would have crashed on your Mac.**

I have updated the following critical files to be "smart" and find their own location:
-   `intelligence_router.py` (The Brain)
-   `Project Midas/main.py` (The Trading Engine)
-   `Project Midas/agents/execution_agent.py` (Buying/Selling)
-   `Project Midas/agents/technical_analyst.py` (Charting)
-   `Project Midas/agents/coach.py` (Strategy)

Now they will work on **both** Windows and Mac automatically.
