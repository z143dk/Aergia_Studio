import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class HealthOpsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AXL Health Ops Dashboard v5.0")
        self.root.geometry("1100x800")
        self.root.configure(bg="#111827") # Dark mode theme

        # Apply styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#111827", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#1f2937", foreground="#ffffff", padding=[15, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])
        self.style.configure("Treeview", background="#1f2937", fieldbackground="#1f2937", foreground="#ffffff")
        self.style.configure("Treeview.Heading", background="#374151", foreground="#ffffff")

        # Initialize local database
        self.init_db()

        # Load settings from db
        self.load_settings()

        # Create tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_checklist = tk.Frame(self.notebook, bg="#111827")
        self.tab_reconstitution = tk.Frame(self.notebook, bg="#111827")
        self.tab_orders = tk.Frame(self.notebook, bg="#111827")
        self.tab_analyzer = tk.Frame(self.notebook, bg="#111827")
        self.tab_baselines = tk.Frame(self.notebook, bg="#111827")
        self.tab_workouts = tk.Frame(self.notebook, bg="#111827")

        self.notebook.add(self.tab_checklist, text="Daily Checklist")
        self.notebook.add(self.tab_reconstitution, text="Reconstitution & Blending")
        self.notebook.add(self.tab_orders, text="Inventory & Re-order Planner")
        self.notebook.add(self.tab_analyzer, text="Redundancy Analyzer")
        self.notebook.add(self.tab_baselines, text="Baseline & Labs")
        self.notebook.add(self.tab_workouts, text="Workouts & Recovery")

        self.setup_checklist_tab()
        self.setup_reconstitution_tab()
        self.setup_orders_tab()
        self.setup_analyzer_tab()
        self.setup_baselines_tab()
        self.setup_workouts_tab()

    def init_db(self):
        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()

        # Create workouts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                workout_type TEXT NOT NULL,
                duration INTEGER,
                avg_hr INTEGER,
                details TEXT
            )
        """)

        # Create recovery_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recovery_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                joint_pain INTEGER,
                soreness INTEGER,
                sleep_quality INTEGER,
                notes TEXT
            )
        """)
        
        # Migration: add weight_lbs column if it does not exist
        try:
            cursor.execute("ALTER TABLE recovery_logs ADD COLUMN weight_lbs REAL")
        except sqlite3.OperationalError:
            pass # Column already exists
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                order_date TEXT NOT NULL,
                quantity_vials INTEGER NOT NULL,
                vial_size_mg REAL NOT NULL,
                dosage_units INTEGER NOT NULL,
                frequency_per_week INTEGER NOT NULL,
                depletion_date TEXT
            )
        """)
        
        # Create settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # Create baselines table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS baselines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marker_name TEXT UNIQUE NOT NULL,
                baseline_value REAL,
                current_value REAL,
                unit TEXT NOT NULL,
                notes TEXT
            )
        """)

        # Create biometrics_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS biometrics_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marker_name TEXT NOT NULL,
                recorded_value REAL NOT NULL,
                recorded_date TEXT NOT NULL,
                notes TEXT
            )
        """)
        
        # Defaults
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('pivot_start_date', ?)", (datetime.now().strftime("%Y-%m-%d"),))
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('last_mots_c_date', '2026-08-08')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('epithalon_active', '0')")
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('ta1_active', '0')")

        # Seed baseline default values
        default_markers = [
            ("HbA1c", 5.4, 5.4, "%", "Blood sugar management marker (Jardiance tracking)"),
            ("eGFR", 92.0, 92.0, "mL/min/1.73m2", "Kidney filtration rate (Renal safety tracker)"),
            ("Total Testosterone", 420.0, 420.0, "ng/dL", "Endocrine pivot target (Clomid/Kisspeptin)"),
            ("LDL Cholesterol", 110.0, 110.0, "mg/dL", "Lipid safety baseline (Atorvastatin tracker)"),
            ("HDL Cholesterol", 45.0, 45.0, "mg/dL", "Lipid safety baseline (Atorvastatin tracker)"),
            ("Resting Heart Rate", 68.0, 68.0, "bpm", "Cardiovascular baseline"),
            ("Systolic BP", 120.0, 120.0, "mmHg", "Blood pressure tracking (Lisinopril tracker)"),
            ("Diastolic BP", 80.0, 80.0, "mmHg", "Blood pressure tracking (Lisinopril tracker)"),
            ("Fasting Glucose", 95.0, 95.0, "mg/dL", "Glucose management (Jardiance tracker)"),
            ("Triglycerides", 150.0, 150.0, "mg/dL", "Lipid safety baseline (Atorvastatin tracker)"),
            ("IGF-1", 150.0, 150.0, "ng/mL", "Growth hormone tracking (Tesamorelin/Ipamorelin)"),
            ("LH", 4.0, 4.0, "mIU/mL", "Luteinizing Hormone (Clomid tracking)"),
            ("FSH", 4.0, 4.0, "mIU/mL", "Follicle-Stimulating Hormone (Clomid tracking)"),
            ("ALT", 25.0, 25.0, "U/L", "Liver function enzyme (Hepatic safety rest)"),
            ("AST", 25.0, 25.0, "U/L", "Liver function enzyme (Hepatic safety rest)"),
            ("Creatinine", 0.9, 0.9, "mg/dL", "Kidney function marker (Renal safety rest)"),
            ("Vitamin B12", 500.0, 500.0, "pg/mL", "B12 levels (Vitamin B12 injection tracker)"),
            ("Vitamin D, 25-OH", 40.0, 40.0, "ng/mL", "Vitamin D levels (Supplement tracker)"),
            ("Magnesium", 2.0, 2.0, "mg/dL", "Magnesium levels (Supplement tracker)"),
            ("Weight", 362.3, 310.0, "lbs", "Bodyweight baseline tracker (Down from 362.3 lbs, -52.3 lbs lost)")
        ]
        for marker, val, cur, unit, notes in default_markers:
            cursor.execute("""
                INSERT OR IGNORE INTO baselines (marker_name, baseline_value, current_value, unit, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (marker, val, cur, unit, notes))
        
        conn.commit()
        conn.close()

    def load_settings(self):
        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        rows = cursor.fetchall()
        self.db_settings = dict(rows)
        conn.close()

    def save_setting(self, key, value):
        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        conn.close()
        self.load_settings()

    # ==================== CHECKLIST TAB ====================
    def setup_checklist_tab(self):
        # Clear tab first in case of reload
        for w in self.tab_checklist.winfo_children():
            w.destroy()

        # Left / Right frames
        left_frame = tk.Frame(self.tab_checklist, bg="#111827")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self.tab_checklist, bg="#1f2937", width=320, padx=15, pady=15)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Title
        title_lbl = tk.Label(left_frame, text="AXL Master Protocol Phase 2 V7 (September Update)", font=("Courier", 15, "bold"), fg="#3b82f6", bg="#111827")
        title_lbl.pack(pady=5, anchor="w")

        # System Time / Status Info
        now_dt = datetime.now()
        day_name = now_dt.strftime("%A")
        
        # Calculate pivot days
        pivot_start = datetime.strptime(self.db_settings.get('pivot_start_date', now_dt.strftime("%Y-%m-%d")), "%Y-%m-%d")
        days_diff = (now_dt - pivot_start).days + 1
        is_kisspeptin_phase = days_diff > 90

        status_text = f"Today is: {day_name} | Day {days_diff} of Endocrine Protocol\n"
        if is_kisspeptin_phase:
            status_text += "Phase: Day 91+ (Kisspeptin-10 & GHK-Cu SubQ Active, Clomid Retired)"
        else:
            status_text += f"Phase: Days 1-90 Pivot (Clomid EOD active, Day {days_diff}/90)"

        status_lbl = tk.Label(left_frame, text=status_text, font=("Arial", 11, "bold"), fg="#10b981", bg="#111827", justify="left")
        status_lbl.pack(pady=5, anchor="w")

        # Re-build checklist dynamically by day
        scroll_canvas = tk.Canvas(left_frame, bg="#111827", highlightthickness=0)
        scroll_canvas.pack(fill="both", expand=True, pady=10)

        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        list_inner = tk.Frame(scroll_canvas, bg="#111827")
        scroll_canvas.create_window((0, 0), window=list_inner, anchor="nw")

        # Determine scheduled compounds based on day
        morning_items = []
        midday_items = []
        night_items = []

        # Baselines
        morning_items.append("Daily Morning Meds: Jardiance (25mg) | Lisinopril (5mg)")
        night_items.append("Daily Nighttime Meds: Atorvastatin (40mg) | Cetirizine HCL (10mg)")

        # Pivot logics
        is_even_day = (days_diff % 2 == 0)
        # Clomid EOD Day logic
        clomid_today = (not is_kisspeptin_phase) and is_even_day
        if clomid_today:
            midday_items.append("Clomid - EOD Midday Window")
        
        # Epithalon/TA1 active cycles
        epithalon_active = self.db_settings.get('epithalon_active') == '1'
        ta1_active = self.db_settings.get('ta1_active') == '1'

        if epithalon_active:
            morning_items.append("🟢 Epithalon: 20 Units (1mg) daily circadian reset")

        if ta1_active and day_name in ["Tuesday", "Thursday", "Saturday"]:
            morning_items.append("🟢 Thymosin Alpha-1 (TA-1): 30 Units (1.5mg) immune management")

        # Schedule router
        if day_name in ["Monday", "Thursday"]: # Wash days
            morning_items.append("🧘 Active Rest: Perform 5-10 mins of light stretching")
            midday_items.append("🏃 Workout: Light Mobility & Active Recovery Stretching (15 mins)")
            
        elif day_name == "Tuesday": # Heavy Peptide Day
            morning_items.extend([
                "🟣 NAD+: 12.5 to 25 Units",
                "🟡 5-Amino-1MQ: 20 Units",
                "🟡 SS-31: 20 Units",
                "🩵 Semax: 5 to 10 Units",
                "🩵 Selank: 5 to 10 Units",
                "💜 Pinealon: 20 Units",
                "🟢 Glutathione: 50 Units (Weekly Dose)"
            ])
            midday_items.extend([
                "🖊️ Mounjaro (Tirzepatide): 2.5mg (1 Pen)",
                "⚪ Lipo-C: 1.0 mL (100 Units)",
                "♦️ Vitamin B12: 0.5 mL (50 Units)",
                "🏋️ Workout: Lower Body & Joint Prep Gym Workout (Leg Press, Extensions, Treadmill progression)"
            ])
            night_items.extend([
                "🔴 Tesamorelin: 25 Units",
                "🔴 Ipamorelin: 5 to 10 Units",
                "🟠 KLOW Blend: 10 Units"
            ])
            if not epithalon_active: # Epithalon pauses DSIP
                night_items.append("🌌 DSIP: 10 Units")
            if is_kisspeptin_phase:
                night_items.append("🩷 Kisspeptin-10: 10 Units (500mcg)")
                night_items.append("🩵 GHK-Cu (SubQ): 5 to 10 Units (1-2mg)")

        elif day_name == "Friday": # Light Peptide Day
            morning_items.extend([
                "🟣 NAD+: 12.5 to 25 Units",
                "🟡 5-Amino-1MQ: 20 Units",
                "🟡 SS-31: 20 Units",
                "🩵 Semax: 5 to 10 Units",
                "🩵 Selank: 5 to 10 Units",
                "💜 Pinealon: 20 Units"
            ])
            midday_items.extend([
                "⚪ Lipo-C: 1.0 mL (100 Units)",
                "♦️ Vitamin B12: 0.5 mL (50 Units)",
                "🏋️ Workout: Lower Body & Joint Prep Gym Workout (Leg Press, Extensions, Treadmill progression)"
            ])
            night_items.extend([
                "🔴 Tesamorelin: 25 Units",
                "🔴 Ipamorelin: 5 to 10 Units",
                "🟠 KLOW Blend: 10 Units"
            ])
            if not epithalon_active: # Epithalon pauses DSIP
                night_items.append("🌌 DSIP: 10 Units")
            if is_kisspeptin_phase:
                night_items.append("🩷 Kisspeptin-10: 10 Units (500mcg)")
                night_items.append("🩵 GHK-Cu (SubQ): 5 to 10 Units (1-2mg)")

        elif day_name in ["Wednesday", "Saturday"]: # Streamlined Health Stack
            morning_items.extend([
                "Base: Molecular Hydrogen Tablet (in water)",
                "TMG (1000mg) - NAD+ Methyl Donor",
                "Hyaluronic Acid (200mg)",
                "🧬 Urolithin A (Mitophagy Support)"
            ])
            midday_items.extend([
                "Base: Animal Pak Powder (in water)",
                "Pure Krill Oil (1 softgel)",
                "Ubiquinol CoQ-10 (100mg)",
                "Astaxanthin (12mg)",
                "Calcium AKG (1000mg)",
                "🧬 Fisetin (Senolytic Support)",
                "Glutathione Triple Boost (1 serving)",
                "🏊 Workout: Upper Body Strength & YMCA Lap Swim"
            ])
            night_items.extend([
                "Base: Collagen Peptides (in water)",
                "Magnesium Glycinate (200–400mg)"
            ])

        elif day_name == "Sunday": # Rest & Recovery (Gym/Pool Closed)
            midday_items.append("🛌 Rest & Recovery: Pure recovery day (YMCA & Gym Closed)")
            if is_kisspeptin_phase:
                night_items.append("🩷 Kisspeptin-10: 10 Units (500mcg)")
                night_items.append("🩵 GHK-Cu (SubQ): 5 to 10 Units (1-2mg)")

        # MOTS-c floater tracker check
        mots_c_sched = self.is_mots_c_scheduled_today()
        if mots_c_sched:
            morning_items.append("🔵 MOTS-c (Floater): 50 Units (Isolated SubQ injection)")

        # Load checked status from database
        today = now_dt.strftime("%Y-%m-%d")
        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS checklist_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, item_text TEXT NOT NULL, checked INTEGER DEFAULT 0, UNIQUE(date, item_text))")
        cursor.execute("SELECT item_text FROM checklist_logs WHERE date=? AND checked=1", (today,))
        checked_today = {r[0] for r in cursor.fetchall()}
        conn.close()

        # Create widgets on list_inner
        # Keep references to variables to prevent garbage collection
        self.checkbox_vars = []

        # Morning Frame
        f_morn = tk.LabelFrame(list_inner, text="☀️ MORNING ROUTINE (Fasted / Empty Stomach)", fg="#60a5fa", bg="#1f2937", padx=10, pady=10, font=("Arial", 11, "bold"))
        f_morn.pack(fill="x", padx=10, pady=5, anchor="w")
        for item in morning_items:
            var = tk.BooleanVar(value=(item in checked_today))
            self.checkbox_vars.append(var)
            cb = tk.Checkbutton(
                f_morn, 
                text=item, 
                variable=var,
                command=lambda val=item, v=var: self.toggle_checklist_item(val, v.get()),
                fg="#ffffff", 
                bg="#1f2937", 
                selectcolor="#111827", 
                activebackground="#1f2937", 
                activeforeground="#ffffff", 
                font=("Arial", 10)
            )
            cb.pack(anchor="w", pady=2)

        # Midday Frame
        f_mid = tk.LabelFrame(list_inner, text="🕒 MIDDAY WINDOW (With Meals / Anytime)", fg="#f59e0b", bg="#1f2937", padx=10, pady=10, font=("Arial", 11, "bold"))
        f_mid.pack(fill="x", padx=10, pady=5, anchor="w")
        if midday_items:
            for item in midday_items:
                var = tk.BooleanVar(value=(item in checked_today))
                self.checkbox_vars.append(var)
                cb = tk.Checkbutton(
                    f_mid, 
                    text=item, 
                    variable=var,
                    command=lambda val=item, v=var: self.toggle_checklist_item(val, v.get()),
                    fg="#ffffff", 
                    bg="#1f2937", 
                    selectcolor="#111827", 
                    activebackground="#1f2937", 
                    activeforeground="#ffffff", 
                    font=("Arial", 10)
                )
                cb.pack(anchor="w", pady=2)
        else:
            tk.Label(f_mid, text="No scheduled Midday tasks today.", fg="#9ca3af", bg="#1f2937", font=("Arial", 10, "italic")).pack(anchor="w")

        # Night Frame
        f_night = tk.LabelFrame(list_inner, text="🌙 NIGHT ROUTINE (Bedtime / Fasted)", fg="#a78bfa", bg="#1f2937", padx=10, pady=10, font=("Arial", 11, "bold"))
        f_night.pack(fill="x", padx=10, pady=5, anchor="w")
        for item in night_items:
            var = tk.BooleanVar(value=(item in checked_today))
            self.checkbox_vars.append(var)
            cb = tk.Checkbutton(
                f_night, 
                text=item, 
                variable=var,
                command=lambda val=item, v=var: self.toggle_checklist_item(val, v.get()),
                fg="#ffffff", 
                bg="#1f2937", 
                selectcolor="#111827", 
                activebackground="#1f2937", 
                activeforeground="#ffffff", 
                font=("Arial", 10)
            )
            cb.pack(anchor="w", pady=2)

        list_inner.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        # Right sidebar widgets: Config Controls
        tk.Label(right_frame, text="PROTOCOL CONTROLS", font=("Arial", 12, "bold"), fg="#ffffff", bg="#1f2937").pack(pady=10)
        
        # Day 1 start picker
        tk.Label(right_frame, text="Day 1 Start Date (YYYY-MM-DD):", fg="#9ca3af", bg="#1f2937").pack(anchor="w", pady=2)
        self.ent_start_date = tk.Entry(right_frame, width=15)
        self.ent_start_date.insert(0, self.db_settings.get('pivot_start_date', now_dt.strftime("%Y-%m-%d")))
        self.ent_start_date.pack(anchor="w", pady=2)
        
        btn_save_date = tk.Button(right_frame, text="Update Start Date", bg="#3b82f6", fg="#ffffff", command=self.update_pivot_start)
        btn_save_date.pack(anchor="w", pady=5)

        # MOTS-c custom button
        tk.Label(right_frame, text="MOTS-c Floater Tracker", font=("Arial", 10, "bold"), fg="#3b82f6", bg="#1f2937").pack(anchor="w", pady=10)
        tk.Label(right_frame, text=f"Last Dose: {self.db_settings.get('last_mots_c_date')}", fg="#9ca3af", bg="#1f2937").pack(anchor="w")
        btn_log_mots = tk.Button(right_frame, text="Log MOTS-c Injection", bg="#10b981", fg="#ffffff", command=self.log_mots_c)
        btn_log_mots.pack(anchor="w", pady=5)

        # Seasonal controls
        tk.Label(right_frame, text="Seasonal Active Toggles", font=("Arial", 10, "bold"), fg="#3b82f6", bg="#1f2937").pack(anchor="w", pady=10)
        
        self.epi_var = tk.BooleanVar(value=epithalon_active)
        cb_epi = tk.Checkbutton(right_frame, text="Epithalon Active (10-Day Cycle)", variable=self.epi_var, command=self.toggle_epithalon, fg="#ffffff", bg="#1f2937", selectcolor="#111827")
        cb_epi.pack(anchor="w")

        self.ta1_var = tk.BooleanVar(value=ta1_active)
        cb_ta1 = tk.Checkbutton(right_frame, text="TA-1 Active (4-6 Wk Cycle)", variable=self.ta1_var, command=self.toggle_ta1, fg="#ffffff", bg="#1f2937", selectcolor="#111827")
        cb_ta1.pack(anchor="w")

        # View Weekly Schedule button
        btn_view_poster = tk.Button(right_frame, text="🖼️ View V7 Master Poster", bg="#3b82f6", fg="#ffffff", font=("Arial", 10, "bold"), command=self.show_master_poster)
        btn_view_poster.pack(anchor="w", pady=5, fill="x")

        btn_view_sched = tk.Button(right_frame, text="📅 View Weekly Schedule", bg="#8b5cf6", fg="#ffffff", font=("Arial", 10, "bold"), command=self.show_full_weekly_schedule)
        btn_view_sched.pack(anchor="w", pady=5, fill="x")

    def update_pivot_start(self):
        val = self.ent_start_date.get().strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            self.save_setting('pivot_start_date', val)
            messagebox.showinfo("Success", f"Endocrine Pivot Day 1 Start Date updated to {val}.")
            self.setup_checklist_tab()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

    def is_mots_c_scheduled_today(self):
        # 5-day cycle: Tuesday -> Sunday -> Friday -> Wednesday -> Monday
        # Calculate matching based on last logged date
        last_str = self.db_settings.get('last_mots_c_date', '2026-08-08')
        try:
            last_date = datetime.strptime(last_str, "%Y-%m-%d")
        except ValueError:
            return False
        
        # MOTS-c occurs exactly every 5 days.
        diff = (datetime.now().date() - last_date.date()).days
        return (diff % 5 == 0)

    def log_mots_c(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        self.save_setting('last_mots_c_date', today_str)
        messagebox.showinfo("Success", f"Logged MOTS-c injection for {today_str}.")
        self.setup_checklist_tab()

    def toggle_epithalon(self):
        val = '1' if self.epi_var.get() else '0'
        self.save_setting('epithalon_active', val)
        self.setup_checklist_tab()

    def toggle_ta1(self):
        val = '1' if self.ta1_var.get() else '0'
        self.save_setting('ta1_active', val)
        self.setup_checklist_tab()

    # ==================== RECONSTITUTION TAB ====================
    def setup_reconstitution_tab(self):
        # Master table display (Read-only reference)
        lbl = tk.Label(self.tab_reconstitution, text="AXL Reconstitution Master Table & Guidelines", font=("Courier", 16, "bold"), fg="#3b82f6", bg="#111827")
        lbl.pack(pady=10)

        # Setup Table Columns
        columns = ("Lid Color", "Compound", "Vial Size", "BAC Water", "Target Dose", "Syringe Draw", "Shelf-Life")
        tree = ttk.Treeview(self.tab_reconstitution, columns=columns, show="headings", height=10)
        tree.pack(fill="x", padx=15, pady=5)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        tree.bind("<Double-1>", self.on_reconstitution_double_click)

        data = [
            ("🟣 RED WINE", "NAD+", "500mg", "2.0 mL", "12.5-25 Units (31-62.5mg)", "12.5-25 Units", "~2.5 Weeks"),
            ("🟡 YELLOW", "5-Amino-1MQ", "50mg", "2.5 mL", "20 Units (4mg)", "20 Units", "~30 Days"),
            ("🟡 YELLOW", "SS-31", "10mg", "2.0 mL", "20 Units (1mg)", "20 Units", "~30 Days"),
            ("🩵 TEAL", "Semax", "10mg", "2.0 mL", "5-10 Units (250-500mcg)", "5-10 Units", "~30 Days"),
            ("🩵 TEAL", "Selank", "10mg", "2.0 mL", "5-10 Units (250-500mcg)", "5-10 Units", "~30 Days"),
            ("💜 PURPLE", "Pinealon", "10mg", "2.0 mL", "20 Units (1mg)", "20 Units", "~30 Days"),
            ("🟢 LT GREEN", "Glutathione", "600mg", "3.0 mL", "50 Units (100mg)", "50 Units", "~30 Days"),
            ("🔴 RED", "Tesamorelin", "10mg", "2.0 mL", "25 Units (1.25mg)", "25 Units", "~2.5 Weeks"),
            ("🔴 RED", "Ipamorelin", "10mg", "2.0 mL", "5-10 Units (250-500mcg)", "5-10 Units", "~30 Days"),
            ("🟠 ORANGE", "KLOW Blend", "80mg", "2.0 mL", "10 Units (0.1 mL)", "10 Units", "~30 Days"),
            ("🌌 NAVY", "DSIP", "10mg", "2.0 mL", "10 Units (500mcg)", "10 Units", "~30 Days"),
            ("🩷 PINK", "Kisspeptin-10", "10mg", "2.0 mL", "10 Units (500mcg)", "10 Units", "~30 Days"),
            ("🩵 VIOLET", "GHK-Cu (SubQ)", "50mg", "2.5-5.0 mL", "5-10 Units (1-2mg)", "5-10 Units", "~30 Days"),
            ("CLEAR", "GHK-Cu (Topical)", "50mg", "2.5-5.0 mL", "1% to 2% Solution", "Pat on skin", "Pat on skin • 30d"),
            ("🔵 BLUE", "MOTS-c", "10mg", "2.0 mL", "50 Units (2.5mg)", "50 Units", "~20 Days"),
            ("⚪ WHITE", "Lipo-C (10mL)", "10 mL Liquid", "Pre-Mixed", "100 Units (1.0 mL)", "100 Units", "Exp. Date on Vial"),
            ("♦️ RUBY", "Vitamin B12", "1mg/mL", "Pre-Mixed", "50 Units (0.5 mL)", "50 Units", "Exp. Date on Vial"),
            ("🖊️ AUTO-PEN", "Mounjaro", "2.5mg Pen", "Pre-Mixed", "1 Pen (2.5mg)", "Auto-Pen", "Single Use")
        ]

        for item in data:
            tree.insert("", "end", values=item)

        # Instructions / Blending rules
        bottom_frame = tk.Frame(self.tab_reconstitution, bg="#1f2937", padx=15, pady=15)
        bottom_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Syringe Compatibility Cards (2 columns)
        compat_left = tk.Frame(bottom_frame, bg="#1f2937")
        compat_left.pack(side="left", fill="both", expand=True, padx=5)

        compat_right = tk.Frame(bottom_frame, bg="#1f2937")
        compat_right.pack(side="right", fill="both", expand=True, padx=5)

        # Left Column: Safe blends
        tk.Label(compat_left, text="✅ SAFE TO BLEND (Shared Syringes)", font=("Arial", 11, "bold"), fg="#10b981", bg="#1f2937").pack(anchor="w", pady=2)
        safe_info = (
            "• Night Growth Stack: Tesamorelin + Ipamorelin (Pituitary Synergism)\n"
            "• Morning Brain Stack: Semax + Selank + Pinealon (Neuro-Compatible)\n"
            "• Fat-Burning Shot: Lipo-C + B12 (Deep SubQ/IM - Requires 3mL syringe)"
        )
        tk.Label(compat_left, text=safe_info, justify="left", fg="#ffffff", bg="#1f2937", font=("Arial", 9)).pack(anchor="w", pady=5)

        # Right Column: Lone wolves
        tk.Label(compat_right, text="🚫 NEVER BLEND (Lone Wolves)", font=("Arial", 11, "bold"), fg="#ef4444", bg="#1f2937").pack(anchor="w", pady=2)
        lone_info = (
            "• NAD+: Highly acidic (pH ~2.5) -> will cook & destroy other peptides\n"
            "• Glutathione: Heavy sulfur content -> degrades amino chains\n"
            "• MOTS-c: Stinging/localized reaction risk -> keep isolated\n"
            "• Mounjaro: FDA-regulated auto-pen device"
        )
        tk.Label(compat_right, text=lone_info, justify="left", fg="#ffffff", bg="#1f2937", font=("Arial", 9)).pack(anchor="w", pady=5)

    # ==================== ORDER TRACKER TAB ====================
    def setup_orders_tab(self):
        for w in self.tab_orders.winfo_children():
            w.destroy()

        title = tk.Label(self.tab_orders, text="Local Supplement & Peptide Order Planner & Pricing", font=("Courier", 16, "bold"), fg="#3b82f6", bg="#111827")
        title.pack(pady=5)

        shipping_lbl = tk.Label(self.tab_orders, text="⚠️ Note: Flat Shipping Fee of $70.00 applies to all orders.", font=("Arial", 11, "bold"), fg="#f59e0b", bg="#111827")
        shipping_lbl.pack(pady=2)

        # Re-order reference list
        reorder_frame = tk.LabelFrame(self.tab_orders, text="Vendor Reference & Re-Order Planning (10-Vial Kits)", fg="#60a5fa", bg="#1f2937", padx=10, pady=10, font=("Arial", 10, "bold"))
        reorder_frame.pack(fill="x", padx=15, pady=5)

        # Table columns for reordering
        ro_cols = ("Compound", "Vendor Code", "Specification", "Kit Price", "Lifespan", "Trigger Month")
        ro_tree = ttk.Treeview(reorder_frame, columns=ro_cols, show="headings", height=8)
        ro_tree.pack(fill="x")

        for col in ro_cols:
            ro_tree.heading(col, text=col)
        ro_tree.column("Compound", width=220, anchor="w")
        ro_tree.column("Vendor Code", width=95, anchor="center")
        ro_tree.column("Specification", width=140, anchor="center")
        ro_tree.column("Kit Price", width=95, anchor="center")
        ro_tree.column("Lifespan", width=160, anchor="center")
        ro_tree.column("Trigger Month", width=110, anchor="center")

        ro_tree.bind("<Double-1>", self.on_vendor_double_click)

        pricing_data = [
            ("Semaglutide", "SM5", "5mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("Semaglutide", "SM10", "10mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("Semaglutide", "SM15", "15mg*10vials", "$60.00", "As Needed", "As Needed"),
            ("Semaglutide", "SM20", "20mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("Semaglutide", "SM30", "30mg*10vials", "$90.00", "As Needed", "As Needed"),
            ("Semaglutide", "SM40", "40mg*10vials", "$110.00", "As Needed", "As Needed"),
            ("Semaglutide", "SM50", "50mg*10vials", "$125.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR5", "5mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR10", "10mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR15", "15mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR20", "20mg*10vials", "$85.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR30", "30mg*10vials", "$100.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR40", "40mg*10vials", "$125.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR50", "50mg*10vials", "$170.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR60", "60mg*10vials", "$190.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR100", "100mg*10vials", "$250.00", "As Needed", "As Needed"),
            ("Tirzepatide", "TR120", "120mg*10vials", "$290.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT5", "5mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT10", "10mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT15", "15mg*10vials", "$110.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT20", "20mg*10vials", "$135.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT30", "30mg*10vials", "$170.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT40", "40mg*10vials", "$205.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT50", "50mg*10vials", "$245.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT60", "60mg*10vials", "$270.00", "As Needed", "As Needed"),
            ("Retatrutide", "RT100", "100mg*10vials", "$360.00", "As Needed", "As Needed"),
            ("Tesamorelin", "TSM2", "2mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Tesamorelin", "TSM5", "5mg*10vials", "$100.00", "As Needed", "As Needed"),
            ("Tesamorelin", "TSM10", "10mg * 10vials", "$180.00", "~26.6 Weeks (6.5 Mo)", "Month 5"),
            ("Tesamorelin", "TSM15", "15mg*10vials", "$250.00", "As Needed", "As Needed"),
            ("Tesamorelin", "TSM20", "20mg*10vials", "$325.00", "As Needed", "As Needed"),
            ("MOTS-c (Human)", "MS5", "5mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("MOTS-c (Human)", "MS10", "10mg * 10vials", "$70.00", "~200 Days (6.5 Mo)", "Month 5"),
            ("MOTS-c (Human)", "MS20", "20mg*10vials", "$115.00", "As Needed", "As Needed"),
            ("MOTS-c (Human)", "MS40", "40mg*10vials", "$180.00", "As Needed", "As Needed"),
            ("GHK-Cu", "Cu50", "50mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("GHK-Cu", "Cu100", "100mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("AHK-CU", "AHK50", "50mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("AHK-CU", "AHK100", "100mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("SS-31", "2S10", "10mg * 10vials", "$90.00", "~33 Weeks (8 Mo)", "Month 6.5"),
            ("SS-31", "2S50", "50mg*10vials", "$290.00", "As Needed", "As Needed"),
            ("GLOW (BPC157+GHK-Cu+TB500)", "GLOW70", "70mg*10vials", "$190.00", "As Needed", "As Needed"),
            ("KLOW Blend", "KLOW80", "80mg * 10vials", "$215.00", "~66 Weeks (15 Mo)", "Month 13"),
            ("IGF-1LR3", "IG01", "0.1mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("IGF-1LR3", "IG1", "1mg*10vials", "$180.00", "As Needed", "As Needed"),
            ("BPC 157", "BC5", "5mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("BPC 157", "BC10", "10mg*10vials", "$65.00", "As Needed", "As Needed"),
            ("BPC 157", "BC20", "20mg*10vials", "$110.00", "As Needed", "As Needed"),
            ("Ipamorelin", "Ipa5", "5mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("Ipamorelin", "Ipa10", "10mg * 10vials", "$70.00", "~66 Weeks (15 Mo)", "Month 13"),
            ("KPV", "KP5", "5mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("KPV", "KP10", "10mg*10vials", "$65.00", "As Needed", "As Needed"),
            ("KPV", "KP30", "30mg*10vials", "$125.00", "As Needed", "As Needed"),
            ("VIP", "VIP5", "5mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("VIP", "VIP10", "10mg*10vials", "$125.00", "As Needed", "As Needed"),
            ("TB500", "TB5", "5mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("TB500", "TB10", "10mg*10vials", "$145.00", "As Needed", "As Needed"),
            ("AOD 9064", "AOD5", "5mg*10vials", "$90.00", "As Needed", "As Needed"),
            ("AOD 9064", "AOD10", "10mg*10vials", "$170.00", "As Needed", "As Needed"),
            ("NAD+", "NJ100", "100mg*10vials", "$25.00", "As Needed", "As Needed"),
            ("NAD+", "NJ500", "500mg * 10vials", "$55.00", "~26.6 Weeks (6.5 Mo)", "Month 5"),
            ("NAD+", "NJ1000", "1000mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("Selank", "sk5", "5mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("Selank", "sk10", "10mg * 10vials", "$55.00", "~66 Weeks (15 Mo)", "Month 13"),
            ("Selank", "sk30", "30mg*10vials", "$145.00", "As Needed", "As Needed"),
            ("Semax", "XA5", "5mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("Semax", "XA10", "10mg * 10vials", "$55.00", "~66 Weeks (15 Mo)", "Month 13"),
            ("Semax", "XA30", "30mg*10vials", "$145.00", "As Needed", "As Needed"),
            ("5-Amino-1MQ", "5AM", "5mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("5-Amino-1MQ", "10AM", "10mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("5-Amino-1MQ", "50AM", "50mg * 10vials", "$90.00", "~40 Weeks (9 Mo)", "Month 7.5"),
            ("Epithalon (Seasonal)", "ET10", "10mg * 10vials", "$55.00", "10 doses/cycle", "As Needed"),
            ("Epithalon", "ET50", "50mg*10vials", "$155.00", "As Needed", "As Needed"),
            ("ARA290 (Cibinetide)", "ARA10", "10mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("Adipotide", "AP5", "5mg*10vials", "$155.00", "As Needed", "As Needed"),
            ("Adipotide", "AP10", "10mg*10vials", "$260.00", "As Needed", "As Needed"),
            ("Aicar", "AR50", "50mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("Aicar", "AR100", "100mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("Vitamin B12", "B12", "1mg/ml", "$55.00", "N/A", "As Needed"),
            ("BPC 5mg + TB 5mg", "BB10", "10mg*10vials", "$100.00", "As Needed", "As Needed"),
            ("BPC 10mg + TB 10mg", "BB20", "20mg*10vials", "$180.00", "As Needed", "As Needed"),
            ("CJC 1295 (No DAC)", "CND2", "2mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("CJC 1295 (No DAC)", "CND5", "5mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("CJC 1295 (No DAC)", "CND10", "10mg*10vials", "$155.00", "As Needed", "As Needed"),
            ("CJC 1295 with DAC", "CD2", "2mg*10vials", "$90.00", "As Needed", "As Needed"),
            ("CJC 1295 with DAC", "CD5", "5mg*10vials", "$160.00", "As Needed", "As Needed"),
            ("CJC 1295 with DAC", "CD10", "10mg*10vials", "$270.00", "As Needed", "As Needed"),
            ("CJC 1295 (No DAC) 5mg+IPA 5mg", "CP10", "10mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("Cagrilintide", "CGL5", "5mg*10vials", "$110.00", "As Needed", "As Needed"),
            ("Cagrilintide", "CGL10", "10mg*10vials", "$180.00", "As Needed", "As Needed"),
            ("Cagrilintide", "CGL20", "20mg*10vials", "$290.00", "As Needed", "As Needed"),
            ("Thymosin Alpha-1 (Seasonal)", "TA10", "10mg * 10vials", "$155.00", "~6 doses/vial", "As Needed"),
            ("Thymosin Alpha-1", "TA5", "5mg*10vials", "$90.00", "As Needed", "As Needed"),
            ("DSIP", "DS5", "5mg*10vials", "$40.00", "As Needed", "As Needed"),
            ("DSIP", "DS10", "10mg * 10vials", "$75.00", "~100 Weeks (23 Mo)", "Month 20"),
            ("DSIP", "DS15", "15mg*10vials", "$115.00", "As Needed", "As Needed"),
            ("FOXO4", "FOX10", "10mg*10vials", "$385.00", "As Needed", "As Needed"),
            ("GHRP-2", "G25", "5mg*10vials", "$40.00", "As Needed", "As Needed"),
            ("GHRP-2", "G210", "10mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("GHRP-6", "G65", "5mg*10vials", "$40.00", "As Needed", "As Needed"),
            ("GHRP-6", "G610", "10mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("LL37", "LL375", "5mg*10vials", "$100.00", "As Needed", "As Needed"),
            ("Melanotan I", "MT1", "10mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Melanotan II", "ML2", "10mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Kisspeptin-10", "KS5", "5mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Kisspeptin-10", "KS10", "10mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("Mazdutide", "MAZ10", "10mg*10vials", "$305.00", "As Needed", "As Needed"),
            ("Oxytocin Acetate", "oxy5", "5mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Oxytocin Acetate", "oxy10", "10mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("Pinealon", "Pin10", "10mg * 10vials", "$70.00", "~33 Weeks (8 Mo)", "Month 6.5"),
            ("Sermorelin Acetate", "Serm5", "5mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("Sermorelin Acetate", "Serm10", "10mg*10vials", "$125.00", "As Needed", "As Needed"),
            ("Snap8", "Snap10", "10mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("Snap8", "Snap20", "20mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("HGH Fragment 176-191", "FRAG5", "5mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("HGH Fragment 176-191", "FRAG10", "10mg*10vials", "$145.00", "As Needed", "As Needed"),
            ("HGH Fragment 176-191", "FRAG12", "12mg*10vials", "$160.00", "As Needed", "As Needed"),
            ("HGH Fragment 176-191", "FRAG15", "15mg*10vials", "$205.00", "As Needed", "As Needed"),
            ("HMG", "G75", "75iu*10vials", "$60.00", "As Needed", "As Needed"),
            ("Hexarelin Acetate", "HX2", "2mg*10vials", "$45.00", "As Needed", "As Needed"),
            ("Hexarelin Acetate", "HX5", "5mg*10vials", "$100.00", "As Needed", "As Needed"),
            ("Lipo-C", "LC10", "10ml * 10vials", "$55.00", "100 Doses (~1 Year)", "Month 10"),
            ("PEG MGF", "PMF2", "2mg*10vials", "$80.00", "As Needed", "As Needed"),
            ("PT141", "PT10", "10mg*10vials", "$65.00", "As Needed", "As Needed"),
            ("Thymalin/Thymulin", "TY10", "10mg*10vials", "$65.00", "As Needed", "As Needed"),
            ("Glutathione", "GTT600", "600mg * 10vials", "$35.00", "~60 Weeks (14 Mo)", "Month 12"),
            ("Glutathione", "GTT1500", "1500mg*10vials", "$65.00", "As Needed", "As Needed"),
            ("Gonadorelin Acetate", "GND2", "2mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("Gonadorelin Acetate", "GND5", "5mg*10vials", "$55.00", "As Needed", "As Needed"),
            ("Survodutide", "SUR10", "10mg*10vials", "$215.00", "As Needed", "As Needed"),
            ("ACE 031", "AC1", "1mg*10vials", "$35.00", "As Needed", "As Needed"),
            ("Cagrisema (2.5mg+2.5mg)", "CS5", "5mg*10vials", "$70.00", "As Needed", "As Needed"),
            ("Cagrisema (5mg+5mg)", "CS10", "10mg*10vials", "$115.00", "As Needed", "As Needed"),
            ("EPO", "EPO3000", "3000iu *10vials", "$60.00", "As Needed", "As Needed"),
            ("Acetic acid 0.6% water", "AA3", "3ml *10vials", "$10.00", "As Needed", "As Needed"),
            ("Acetic acid 0.6% water", "AA5", "5ml*10vials", "$15.00", "As Needed", "As Needed"),
            ("Acetic acid 0.6% water", "AA10", "10ml*10vials", "$20.00", "As Needed", "As Needed"),
            ("Lemon Bottle", "LB10", "10ml*10vials", "$55.00", "As Needed", "As Needed"),
            ("Bacteriostatic Water", "BAC3", "3ml *10vials", "$10.00", "As Needed", "As Needed"),
            ("Bacteriostatic Water", "BAC10", "10ml * 10vials", "$15.00", "N/A", "As Needed")
        ]
        for row in pricing_data:
            ro_tree.insert("", "end", values=row)

        # Logging input UI
        input_frame = tk.Frame(self.tab_orders, bg="#1f2937", padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(input_frame, text="Item Name:", fg="#ffffff", bg="#1f2937").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.entry_item = tk.Entry(input_frame, width=15)
        self.entry_item.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Vials Count:", fg="#ffffff", bg="#1f2937").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.entry_vials = tk.Entry(input_frame, width=8)
        self.entry_vials.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Vial Size (mg):", fg="#ffffff", bg="#1f2937").grid(row=0, column=4, padx=5, pady=2, sticky="e")
        self.entry_size = tk.Entry(input_frame, width=8)
        self.entry_size.grid(row=0, column=5, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Dose (Units):", fg="#ffffff", bg="#1f2937").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.entry_dose = tk.Entry(input_frame, width=15)
        self.entry_dose.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Weekly Freq:", fg="#ffffff", bg="#1f2937").grid(row=1, column=2, padx=5, pady=2, sticky="e")
        self.entry_freq = tk.Entry(input_frame, width=8)
        self.entry_freq.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        btn_add = tk.Button(input_frame, text="LOG ORDER", font=("Arial", 9, "bold"), fg="#ffffff", bg="#10b981", command=self.add_order)
        btn_add.grid(row=1, column=4, columnspan=2, padx=10, pady=2, sticky="we")

        # Calculator label in row 2
        self.lbl_bac_calc = tk.Label(input_frame, text="Reconstitution Guidance: Select or type values to calculate", fg="#60a5fa", bg="#1f2937", font=("Arial", 10, "italic"), justify="left")
        self.lbl_bac_calc.grid(row=2, column=0, columnspan=6, pady=5, sticky="w")

        # Key release binds to auto-calculate reconstitution and pricing
        self.entry_item.bind("<KeyRelease>", self.recalculate_reconstitution)
        self.entry_vials.bind("<KeyRelease>", self.recalculate_reconstitution)
        self.entry_size.bind("<KeyRelease>", self.recalculate_reconstitution)
        self.entry_dose.bind("<KeyRelease>", self.recalculate_reconstitution)

        # Logged table display
        self.tree_frame = tk.Frame(self.tab_orders, bg="#111827")
        self.tree_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Item", "Ordered", "Qty", "Dose", "Freq", "Est. Depletion"), show="headings", height=5)
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("Item", text="Compound/Supplement")
        self.tree.heading("Ordered", text="Order Date")
        self.tree.heading("Qty", text="Vials")
        self.tree.heading("Dose", text="Dose (U)")
        self.tree.heading("Freq", text="Freq/Wk")
        self.tree.heading("Est. Depletion", text="Est. Depletion")

        self.tree.column("Item", width=180, anchor="center")
        self.tree.column("Ordered", width=100, anchor="center")
        self.tree.column("Qty", width=60, anchor="center")
        self.tree.column("Dose", width=80, anchor="center")
        self.tree.column("Freq", width=80, anchor="center")
        self.tree.column("Est. Depletion", width=140, anchor="center")

        scrollbar_tree = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_tree.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_tree.set)

        self.load_orders()

    def add_order(self):
        try:
            item = self.entry_item.get()
            vials = int(self.entry_vials.get())
            size = float(self.entry_size.get())
            dose = int(self.entry_dose.get())
            freq = int(self.entry_freq.get())
            
            if not item:
                raise ValueError("Item name is required.")

            order_date = datetime.now().strftime("%Y-%m-%d")

            # Standard reconstitution of 2mL (200 Units) per vial
            total_units_available = vials * 200
            weekly_consumption_units = dose * freq
            
            if weekly_consumption_units > 0:
                weeks_lasting = total_units_available / weekly_consumption_units
                days_lasting = int(weeks_lasting * 7)
                depletion_dt = datetime.now() + timedelta(days=days_lasting)
                depletion_date_str = depletion_dt.strftime("%Y-%m-%d")
            else:
                depletion_date_str = "N/A (No Frequency)"

            conn = sqlite3.connect("health_ops.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (item_name, order_date, quantity_vials, vial_size_mg, dosage_units, frequency_per_week, depletion_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item, order_date, vials, size, dose, freq, depletion_date_str))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Logged order for {item}. Est. depletion: {depletion_date_str}")
            self.setup_orders_tab()

        except Exception as e:
            messagebox.showerror("Input Error", f"Please verify inputs.\n{str(e)}")

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, order_date, quantity_vials, dosage_units, frequency_per_week, depletion_date FROM orders")
        rows = cursor.fetchall()
        for r in rows:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], r[5]))
        conn.close()

    # ==================== ANALYZER TAB ====================
    def setup_analyzer_tab(self):
        title = tk.Label(self.tab_analyzer, text="Clinical Redundancy & Safety Analyzer", font=("Courier", 16, "bold"), fg="#3b82f6", bg="#111827")
        title.pack(pady=10)

        desc = tk.Label(self.tab_analyzer, text="Select the compounds you are currently taking to scan for cell, receptor, or organ pathway conflicts.", wraplength=800, justify="center", fg="#9ca3af", bg="#111827", font=("Arial", 10))
        desc.pack(pady=5)

        scroll_canvas = tk.Canvas(self.tab_analyzer, bg="#111827", highlightthickness=0)
        scroll_canvas.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(self.tab_analyzer, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(scroll_canvas, bg="#111827")
        scroll_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.compounds = {
            "Mounjaro (Tirzepatide)": tk.BooleanVar(),
            "Semaglutide (Ozempic/Wegovy)": tk.BooleanVar(),
            "Retatrutide": tk.BooleanVar(),
            "Tesamorelin": tk.BooleanVar(),
            "CJC-1295 (No DAC)": tk.BooleanVar(),
            "Sermorelin": tk.BooleanVar(),
            "Ipamorelin": tk.BooleanVar(),
            "BPC-157 (Standalone)": tk.BooleanVar(),
            "TB-500 (Standalone)": tk.BooleanVar(),
            "KLOW Blend (GHK-Cu, BPC-157, TB-500, KPV)": tk.BooleanVar(),
            "NAD+ (Injectable)": tk.BooleanVar(),
            "5-Amino-1MQ": tk.BooleanVar(),
            "SS-31 (Elamipretide)": tk.BooleanVar(),
            "MOTS-c": tk.BooleanVar(),
            "Jardiance (Empagliflozin)": tk.BooleanVar()
        }

        row = 0
        col = 0
        for name, var in self.compounds.items():
            cb = tk.Checkbutton(self.inner_frame, text=name, variable=var, fg="#ffffff", bg="#111827", selectcolor="#1f2937", activebackground="#111827", activeforeground="#ffffff", font=("Arial", 11))
            cb.grid(row=row, column=col, sticky="w", padx=20, pady=5)
            col += 1
            if col > 1:
                col = 0
                row += 1

        self.inner_frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        btn_analyze = tk.Button(self.tab_analyzer, text="RUN CONFLICT ANALYSIS", font=("Arial", 11, "bold"), fg="#ffffff", bg="#3b82f6", activebackground="#2563eb", activeforeground="#ffffff", command=self.run_analysis)
        btn_analyze.pack(pady=15)

    def run_analysis(self):
        active = [name for name, var in self.compounds.items() if var.get()]
        conflicts = []

        glp1_count = sum(1 for x in ["Mounjaro (Tirzepatide)", "Semaglutide (Ozempic/Wegovy)", "Retatrutide"] if x in active)
        if glp1_count > 1:
            conflicts.append("⚠️ **GLP-1 Receptor Agonist Overload:** Multiple heavy-tier glycemic/weight loss agonists selected. Combining Tirzepatide, Semaglutide, or Retatrutide is highly redundant and increases severe gastrointestinal and glycemic risks.")

        ghrh_count = sum(1 for x in ["Tesamorelin", "CJC-1295 (No DAC)", "Sermorelin"] if x in active)
        if ghrh_count > 1:
            conflicts.append("⚠️ **Pituitary GHRH Receptor Overlap:** You have selected multiple Growth Hormone-Releasing Hormone analogs (e.g. CJC-1295, Tesamorelin, Sermorelin). These target the exact same pituitary receptors, causing redundant competition and rapid desensitization.")

        healing_overlap = ("KLOW Blend (GHK-Cu, BPC-157, TB-500, KPV)" in active) and ("BPC-157 (Standalone)" in active or "TB-500 (Standalone)" in active)
        if healing_overlap:
            conflicts.append("⚠️ **Tissue-Repair Redundancy:** Standard standalone BPC-157 or TB-500 overlaps with your KLOW Blend, which already contains both compounds. Avoid double-dosing these regenerative pathways.")

        mito_count = sum(1 for x in ["NAD+ (Injectable)", "5-Amino-1MQ", "SS-31 (Elamipretide)", "MOTS-c"] if x in active)
        if mito_count > 2:
            conflicts.append("⚠️ **Mitochondrial Overstimulation Alert:** Stacking NAD+, 5-Amino-1MQ, SS-31, and MOTS-c simultaneously places intense metabolic demands on your cell-clearing pathways. Consider a structured cycle (e.g., SS-31 first to repair, then MOTS-c to accelerate).")

        if "Jardiance (Empagliflozin)" in active and "Mounjaro (Tirzepatide)" in active:
            conflicts.append("ℹ️ **Prescription Co-Administration Sync:** Combining SGLT2 inhibitors (Jardiance) and GLP-1/GIP agonists (Mounjaro) requires careful tracking of your HbA1c and hydration levels. Ensure your physician has cleared your kidney filtration values (eGFR).")

        if not conflicts:
            messagebox.showinfo("Analysis Complete", "✅ No critical compound or receptor redundancies detected. Your selected stack represents distinct, non-overlapping physiological pathways.")
        else:
            conflict_msg = "\n\n".join(conflicts)
            messagebox.showwarning("Redundancy/Safety Flags Found", f"The following pathways require attention and doctor correlation:\n\n{conflict_msg}")

    # ==================== BASELINES & LABS TAB ====================
    def setup_baselines_tab(self):
        # Clear tab first in case of reload
        for w in self.tab_baselines.winfo_children():
            w.destroy()

        # Left / Right frames
        left_frame = tk.Frame(self.tab_baselines, bg="#111827")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self.tab_baselines, bg="#1f2937", width=340, padx=15, pady=15)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Title
        title_lbl = tk.Label(left_frame, text="AXL Baseline & Labs Tracker", font=("Courier", 16, "bold"), fg="#3b82f6", bg="#111827")
        title_lbl.pack(pady=5, anchor="w")

        # Table columns for baselines
        cols = ("Marker", "Baseline", "Current", "Unit", "Variance", "Notes")
        self.base_tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=15)
        self.base_tree.pack(fill="both", expand=True, pady=5)

        for col in cols:
            self.base_tree.heading(col, text=col)
            self.base_tree.column(col, width=110, anchor="center")
        self.base_tree.column("Notes", width=250, anchor="w")
        self.base_tree.column("Marker", width=150, anchor="w")

        self.base_tree.bind("<<TreeviewSelect>>", self.on_marker_select)
        self.base_tree.bind("<Double-1>", self.on_baseline_double_click)

        # Add scrollbar to tree
        tree_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.base_tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.base_tree.configure(yscrollcommand=tree_scroll.set)

        # Right side: Add / Update Forms
        tk.Label(right_frame, text="LOG NEW READING", font=("Arial", 12, "bold"), fg="#ffffff", bg="#1f2937").pack(pady=10)

        # Selected marker indicator
        self.lbl_selected_marker = tk.Label(right_frame, text="Select a marker on the left", font=("Arial", 11, "italic"), fg="#9ca3af", bg="#1f2937")
        self.lbl_selected_marker.pack(pady=5)

        tk.Label(right_frame, text="Value:", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.entry_marker_val = tk.Entry(right_frame, width=20)
        self.entry_marker_val.pack(anchor="w", pady=2)

        tk.Label(right_frame, text="Date (YYYY-MM-DD):", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.entry_marker_date = tk.Entry(right_frame, width=20)
        self.entry_marker_date.pack(anchor="w", pady=2)
        self.entry_marker_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(right_frame, text="Log Notes / Lab Context:", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.entry_marker_notes = tk.Entry(right_frame, width=30)
        self.entry_marker_notes.pack(anchor="w", pady=2)

        btn_log_val = tk.Button(right_frame, text="Save Reading", bg="#10b981", fg="#ffffff", font=("Arial", 9, "bold"), command=self.log_biometric)
        btn_log_val.pack(anchor="w", pady=10, fill="x")

        # Baseline adjustment form
        tk.Label(right_frame, text="ADJUST REFERENCE BASELINE", font=("Arial", 10, "bold"), fg="#3b82f6", bg="#1f2937").pack(anchor="w", pady=10)
        
        tk.Label(right_frame, text="New Baseline Value:", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.entry_new_base = tk.Entry(right_frame, width=20)
        self.entry_new_base.pack(anchor="w", pady=2)

        btn_update_base = tk.Button(right_frame, text="Update Baseline Reference", bg="#3b82f6", fg="#ffffff", font=("Arial", 9), command=self.update_baseline_reference)
        btn_update_base.pack(anchor="w", pady=5, fill="x")

        # History log section
        tk.Label(right_frame, text="HISTORICAL READINGS", font=("Arial", 10, "bold"), fg="#a78bfa", bg="#1f2937").pack(anchor="w", pady=10)
        
        self.txt_marker_history = tk.Text(right_frame, height=8, width=35, bg="#111827", fg="#ffffff", font=("Arial", 9))
        self.txt_marker_history.pack(fill="both", expand=True, pady=5)
        self.txt_marker_history.config(state="disabled")

        self.load_baselines()

    def load_baselines(self):
        # Clear tree
        for row in self.base_tree.get_children():
            self.base_tree.delete(row)

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("SELECT marker_name, baseline_value, current_value, unit, notes FROM baselines")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            marker, val, cur, unit, notes = r
            # Calculate variance
            variance = ""
            if val is not None and cur is not None:
                if val != 0:
                    diff_pct = ((cur - val) / val) * 100
                    variance = f"{diff_pct:+.1f}%"
                else:
                    variance = f"{cur - val:+.1f}"

            self.base_tree.insert("", "end", values=(marker, val, cur, unit, variance, notes))

    def on_marker_select(self, event):
        selected = self.base_tree.selection()
        if not selected:
            return
        item = self.base_tree.item(selected[0])
        marker = item['values'][0]
        base_val = item['values'][1]

        self.lbl_selected_marker.config(text=f"Selected: {marker}", font=("Arial", 11, "bold"), fg="#10b981")
        self.entry_new_base.delete(0, tk.END)
        self.entry_new_base.insert(0, str(base_val))

        # Load history text
        self.load_marker_history(marker)

    def on_baseline_double_click(self, event):
        tree = event.widget
        selected = tree.selection()
        if not selected:
            return
        
        item_vals = tree.item(selected[0])['values']
        marker = item_vals[0]
        current_val = item_vals[2]
        unit = item_vals[3]
        
        # Open simpledialog prompt
        from tkinter import simpledialog
        try:
            init_val = float(current_val) if current_val else 0.0
        except ValueError:
            init_val = 0.0

        new_val = simpledialog.askfloat("Quick Lab Log", f"Enter new value for {marker} ({unit}):", initialvalue=init_val)
        
        if new_val is not None:
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect("health_ops.db")
            cursor = conn.cursor()
            
            # Update current value
            cursor.execute("""
                UPDATE baselines 
                SET current_value = ? 
                WHERE marker_name = ?
            """, (new_val, marker))
            
            # Log in biometrics_history
            cursor.execute("""
                INSERT INTO biometrics_history (marker_name, recorded_value, recorded_date, notes)
                VALUES (?, ?, ?, 'Logged via double-click baseline shortcut')
            """, (marker, new_val, today))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Recorded {marker} value of {new_val} {unit} successfully!")
            self.load_baselines()
            self.load_marker_history(marker)

    def load_marker_history(self, marker):
        self.txt_marker_history.config(state="normal")
        self.txt_marker_history.delete("1.0", tk.END)

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT recorded_value, recorded_date, notes 
            FROM biometrics_history 
            WHERE marker_name = ? 
            ORDER BY recorded_date DESC
        """, (marker,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            self.txt_marker_history.insert(tk.END, "No historical entries logged yet.")
        else:
            for r in rows:
                self.txt_marker_history.insert(tk.END, f"[{r[1]}] {r[0]} | {r[2]}\n")

        self.txt_marker_history.config(state="disabled")

    def log_biometric(self):
        selected = self.base_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a marker from the table first.")
            return

        marker = self.base_tree.item(selected[0])['values'][0]
        val_str = self.entry_marker_val.get().strip()
        date_str = self.entry_marker_date.get().strip()
        notes_str = self.entry_marker_notes.get().strip()

        try:
            val = float(val_str)
            # Basic date validation
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Please verify inputs. Value must be numeric and date must be YYYY-MM-DD.")
            return

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        # Add to history
        cursor.execute("""
            INSERT INTO biometrics_history (marker_name, recorded_value, recorded_date, notes)
            VALUES (?, ?, ?, ?)
        """, (marker, val, date_str, notes_str))
        # Update current value in baselines
        cursor.execute("""
            UPDATE baselines 
            SET current_value = ? 
            WHERE marker_name = ?
        """, (val, marker))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Logged {val} for {marker}.")
        self.entry_marker_val.delete(0, tk.END)
        self.entry_marker_notes.delete(0, tk.END)
        self.load_baselines()
        self.load_marker_history(marker)

    def update_baseline_reference(self):
        selected = self.base_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a marker from the table first.")
            return

        marker = self.base_tree.item(selected[0])['values'][0]
        new_base_str = self.entry_new_base.get().strip()

        try:
            new_base = float(new_base_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for the baseline.")
            return

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE baselines 
            SET baseline_value = ? 
            WHERE marker_name = ?
        """, (new_base, marker))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Reference baseline for {marker} updated to {new_base}.")
        self.load_baselines()

    def show_full_weekly_schedule(self):
        sched_win = tk.Toplevel(self.root)
        sched_win.title("AXL Protocol - Full Weekly Schedule")
        sched_win.geometry("900x700")
        sched_win.configure(bg="#111827")

        # Scrollable Text Widget
        frame = tk.Frame(sched_win, bg="#111827")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        txt = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set, bg="#1f2937", fg="#ffffff", insertbackground="white", font=("Courier", 10), padx=10, pady=10)
        txt.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=txt.yview)

        schedule_text = """🧬 AXL MASTER PROTOCOL: PHASE 2 V5 WEEKLY SCHEDULE
===================================================

🛑 MONDAY & THURSDAY: THE WASH DAYS (Hepatic & Renal Rest)
-----------------------------------------------------------
• Morning: Daily Morning Meds ONLY (Jardiance 25mg | Lisinopril 5mg)
• Midday: Clomid (ONLY if EOD during Days 1–90)
• Night: Daily Night Meds ONLY (Atorvastatin 40mg | Cetirizine HCL 10mg)

💉 TUESDAY: HEAVY PEPTIDE DAY
------------------------------
• Morning (Fasted): 
  - Daily Meds (Jardiance | Lisinopril)
  - NAD+ (12.5-25 Units / 31-62.5mg)
  - 5-Amino-1MQ (20 Units / 4mg)
  - SS-31 (20 Units / 1mg)
  - Semax (5-10 Units / 250-500mcg)
  - Selank (5-10 Units / 250-500mcg)
  - Pinealon (20 Units / 1mg)
  - Glutathione (50 Units / 100mg)
• Midday / Anytime: 
  - Clomid (if EOD)
  - Mounjaro (2.5mg Pen)
  - Lipo-C (100 Units / 1.0 mL)
  - Vitamin B12 (50 Units / 0.5 mL)
• Night (Fasted): 
  - Daily Meds (Atorvastatin | Cetirizine HCL)
  - Tesamorelin (25 Units / 1.25mg)
  - Ipamorelin (5-10 Units / 250-500mcg)
  - KLOW Blend (10 Units / 0.1 mL)
  - DSIP (10 Units / 500mcg)
  - Kisspeptin (5-10 Units / 250-500mcg - Day 91+)

🌿 WEDNESDAY & SATURDAY: STREAMLINED HEALTH STACK
-------------------------------------------------
• Morning Window (Empty Stomach): 
  - Daily Meds
  - Molecular Hydrogen Tablet
  - TMG (1000mg)
  - Hyaluronic Acid (200mg)
  - Urolithin A
• Midday Window (With Dietary Fats/Meal): 
  - Clomid (if EOD)
  - Animal Pak Powder
  - Pure Krill Oil
  - Ubiquinol CoQ-10 (100mg)
  - Astaxanthin (12mg)
  - Calcium AKG (1000mg)
  - Fisetin
  - Glutathione Triple Boost
• Night Window (Bedtime): 
  - Daily Meds
  - Micro Ingredients Multi Collagen Peptides
  - Magnesium Glycinate (200–400mg)

💉 FRIDAY & SUNDAY: LIGHT PEPTIDE DAYS
---------------------------------------
• Morning (Fasted): 
  - Daily Meds
  - NAD+ (12.5-25 Units)
  - 5-Amino-1MQ (20 Units)
  - SS-31 (20 Units)
  - Semax (5-10 Units)
  - Selank (5-10 Units)
  - Pinealon (20 Units)
• Midday / Anytime: 
  - Clomid (if EOD)
  - Lipo-C (100 Units / 1.0 mL)
  - Vitamin B12 (50 Units / 0.5 mL - Friday Only)
• Night (Fasted): 
  - Daily Meds
  - Tesamorelin (25 Units)
  - Ipamorelin (5-10 Units)
  - KLOW Blend (10 Units)
  - DSIP (10 Units - Friday Only)
  - Kisspeptin (5-10 Units - Day 91+)

⚠️ FLOATER & SEASONAL CYCLES (Tracked separately)
-------------------------------------------------
• MOTS-c (5-Day Rule): 50 Units in morning (Tuesday → Sunday → Friday → Wednesday → Monday). Take isolated if landing on a Wash Day.
• Epithalon: 20 Units (1mg) daily for 10 days straight (1-2x/year during Equinox transitions). Pause DSIP while running.
• Thymosin Alpha-1 (TA-1): 30 Units (1.5mg) 2-3x weekly for 4-6 weeks (followed by mandatory 3-month break).
"""
        txt.insert(tk.END, schedule_text)
        txt.config(state="disabled")

    def on_vendor_double_click(self, event):
        tree = event.widget
        selected = tree.selection()
        if not selected:
            return
        
        item_vals = tree.item(selected[0])['values']
        compound = item_vals[0]
        
        # Default specifications map for known protocol compounds
        defaults_map = {
            "Tesamorelin": (10, 10.0, 25, 3),
            "Ipamorelin": (10, 10.0, 10, 3),
            "NAD+": (10, 500.0, 25, 3),
            "MOTS-c": (10, 10.0, 50, 1),
            "SS-31": (10, 10.0, 20, 3),
            "5-Amino-1MQ": (10, 50.0, 20, 3),
            "Semax": (10, 10.0, 10, 3),
            "Selank": (10, 10.0, 10, 3),
            "Pinealon": (10, 10.0, 20, 3),
            "DSIP": (10, 10.0, 10, 2),
            "KLOW Blend": (10, 80.0, 10, 3),
            "Glutathione": (10, 600.0, 50, 1),
            "Epithalon (Seasonal)": (10, 10.0, 20, 7),
            "Thymosin Alpha-1 (Seasonal)": (10, 10.0, 30, 3),
            "Lipo-C": (10, 10.0, 100, 3),
            "Vitamin B12": (10, 1.0, 50, 2),
            "BAC Water": (10, 10.0, 0, 0)
        }
        
        # Clear fields
        self.entry_item.delete(0, tk.END)
        self.entry_vials.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.entry_dose.delete(0, tk.END)
        self.entry_freq.delete(0, tk.END)
        
        # Parse price
        try:
            price_str = str(item_vals[3]).replace("$", "").strip()
            self.last_selected_kit_price = float(price_str)
        except Exception:
            self.last_selected_kit_price = 0.0
            
        # Populate
        self.entry_item.insert(0, compound)
        
        # Check standard defaults first
        matched_key = None
        for k in defaults_map.keys():
            if k.lower() in compound.lower():
                matched_key = k
                break
                
        if matched_key:
            vials, size, dose, freq = defaults_map[matched_key]
        else:
            # Parse specification
            spec = str(item_vals[2]) # e.g. "10mg*10vials", "75iu*10vials"
            vials = 10
            # Try to extract vial count
            if "*10" in spec or "10vials" in spec:
                vials = 10
            
            # Try to extract vial size
            size = 10.0 # fallback
            for unit in ["mg", "ml", "iu"]:
                if unit in spec.lower():
                    try:
                        size = float(spec.lower().split(unit)[0].strip())
                        break
                    except ValueError:
                        pass
            
            # Set default dose & frequency based on compound name
            dose = 10 # default
            freq = 3 # default 3x a week
            
            # If weight loss / glycemic peptide (Semaglutide, Tirzepatide, Retatrutide, Cagrilintide)
            glycemic_keywords = ["semaglutide", "tirzepatide", "retatrutide", "cagrilintide", "cagrisema", "mazdutide", "survodutide", "adipotide"]
            if any(kw in compound.lower() for kw in glycemic_keywords):
                dose = 10
                freq = 1 # once a week
            elif "mots-c" in compound.lower():
                dose = 50
                freq = 1
            elif "glutathione" in compound.lower():
                dose = 50
                freq = 1
                
        self.entry_vials.insert(0, str(vials))
        self.entry_size.insert(0, str(size))
        self.entry_dose.insert(0, str(dose))
        self.entry_freq.insert(0, str(freq))
        
        # Trigger dynamic calculation immediately
        self.recalculate_reconstitution()

    def recalculate_reconstitution(self, event=None):
        item = self.entry_item.get().strip().lower()
        size_str = self.entry_size.get().strip()
        dose_str = self.entry_dose.get().strip()
        vials_str = self.entry_vials.get().strip()

        if not item:
            self.last_selected_kit_price = 0.0

        if not size_str:
            # Still display pricing even if reconstitution size is missing
            pricing_text = ""
            if hasattr(self, 'last_selected_kit_price') and self.last_selected_kit_price > 0:
                try:
                    vials = int(vials_str) if vials_str else 10
                except ValueError:
                    vials = 10
                kits = max(1, int(vials / 10))
                base_cost = kits * self.last_selected_kit_price
                shipping = 70.00
                total = base_cost + shipping
                pricing_text = f"\nPrice: {kits} Kit(s) @ ${self.last_selected_kit_price:.2f}/ea = ${base_cost:.2f} | Shipping: ${shipping:.2f} | Total: ${total:.2f}"
            self.lbl_bac_calc.config(text=f"Enter Vial Size and Target Dose to calculate BAC water.{pricing_text}", fg="#9ca3af")
            return

        try:
            size = float(size_str)
        except ValueError:
            self.lbl_bac_calc.config(text="Vial Size must be a valid number.", fg="#ef4444")
            return

        try:
            dose_units = float(dose_str) if dose_str else 0.0
        except ValueError:
            dose_units = 0.0

        # Protocol mapping for known reconstitution water
        known_bac_map = {
            "nad+": 2.0,
            "5-amino-1mq": 2.5,
            "ss-31": 2.0,
            "semax": 2.0,
            "selank": 2.0,
            "pinealon": 2.0,
            "glutathione": 3.0,
            "tesamorelin": 2.0,
            "ipamorelin": 2.0,
            "klow blend": 2.0,
            "dsip": 2.0,
            "kisspeptin": 2.0,
            "mots-c": 2.0,
            "lipo-c": 0.0, # Pre-mixed
            "vitamin b12": 0.0, # Pre-mixed
            "mounjaro": 0.0, # Pre-mixed
            "bpc 157": 2.0,
            "tb500": 2.0,
            "ghk-cu": 2.0,
            "cjc 1295": 2.0,
            "cjc1295": 2.0,
            "sermorelin": 2.0,
            "epithalon": 2.0,
            "thymosin alpha 1": 2.0,
            "ta1": 2.0,
            "bpc": 2.0
        }

        # Find match in known map
        matched_item = None
        for k, v in known_bac_map.items():
            if k in item:
                matched_item = k
                break

        # Calculate recommended BAC water
        is_premixed = False
        if matched_item in ["lipo-c", "vitamin b12", "mounjaro"] or "pre-mixed" in item or "premixed" in item or "liquid" in item:
            is_premixed = True
            bac_water = 0.0
        elif matched_item:
            bac_water = known_bac_map[matched_item]
        else:
            # Dynamic calculation: target a standard 5.0 mg/mL concentration for general peptides
            if size == 0:
                bac_water = 2.0
            else:
                bac_water = size / 5.0 # targeting 5 mg/mL
                # Round to standard increments (1.0, 2.0, 3.0, 5.0)
                if bac_water < 1.0:
                    bac_water = 1.0
                elif bac_water <= 2.0:
                    bac_water = 2.0
                elif bac_water <= 3.0:
                    bac_water = 3.0
                elif bac_water <= 5.0:
                    bac_water = 5.0
                else:
                    bac_water = round(bac_water * 2) / 2 # round to nearest 0.5

        # Calculate pricing text if last selected kit price is set
        pricing_text = ""
        if hasattr(self, 'last_selected_kit_price') and self.last_selected_kit_price > 0:
            try:
                vials = int(vials_str) if vials_str else 10
            except ValueError:
                vials = 10
            kits = max(1, int(vials / 10))
            base_cost = kits * self.last_selected_kit_price
            shipping = 70.00
            total = base_cost + shipping
            pricing_text = f"\nPrice: {kits} Kit(s) @ ${self.last_selected_kit_price:.2f}/ea = ${base_cost:.2f} | Shipping: ${shipping:.2f} | Total: ${total:.2f}"

        if is_premixed:
            self.lbl_bac_calc.config(text=f"Pre-Mixed Liquid: No reconstitution (BAC water) required.{pricing_text}", fg="#10b981")
            return

        if bac_water > 0:
            conc = size / bac_water # mg/mL
            
            # Calculate dose in mg or mcg
            if dose_units > 0:
                dose_mg = (dose_units / 100.0) * conc
                if dose_mg < 1.0:
                    dose_display = f"{dose_mg * 1000:.0f} mcg"
                else:
                    dose_display = f"{dose_mg:.2f} mg"
                
                self.lbl_bac_calc.config(
                    text=f"Reconstitution: Add {bac_water:.1f} mL BAC Water | Conc: {conc:.1f} mg/mL | Dose: {dose_display} per {int(dose_units)} Units draw{pricing_text}",
                    fg="#3b82f6"
                )
            else:
                self.lbl_bac_calc.config(
                    text=f"Reconstitution Suggestion: Add {bac_water:.1f} mL BAC Water | Yields Conc: {conc:.1f} mg/mL{pricing_text}",
                    fg="#60a5fa"
                )
        else:
            self.lbl_bac_calc.config(text=f"Enter Vial Size and Target Dose to calculate BAC water.{pricing_text}", fg="#9ca3af")

    # ==================== WORKOUTS & RECOVERY TAB ====================
    def setup_workouts_tab(self):
        # Clear tab first in case of reload
        for w in self.tab_workouts.winfo_children():
            w.destroy()

        # Left / Right frames
        left_frame = tk.Frame(self.tab_workouts, bg="#111827")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self.tab_workouts, bg="#1f2937", width=360, padx=15, pady=15)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # LEFT COLUMN: WORKOUT LOGGER
        title_lbl = tk.Label(left_frame, text="AXL Phase 1 Training Logger", font=("Courier", 16, "bold"), fg="#3b82f6", bg="#111827")
        title_lbl.pack(pady=5, anchor="w")

        # Form fields
        form_frame = tk.Frame(left_frame, bg="#1f2937", padx=10, pady=10)
        form_frame.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Workout Type:", fg="#ffffff", bg="#1f2937").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_workout_type = ttk.Combobox(form_frame, values=[
            "Lower Body & Joint Prep",
            "Upper Body & Calisthenics",
            "YMCA Lap Swim",
            "Light Mobility",
            "Rest & Recovery"
        ], state="readonly", width=25)
        self.combo_workout_type.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo_workout_type.set("Lower Body & Joint Prep")

        tk.Label(form_frame, text="Duration (mins):", fg="#ffffff", bg="#1f2937").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_workout_dur = tk.Entry(form_frame, width=10)
        self.entry_workout_dur.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_workout_dur.insert(0, "30")

        tk.Label(form_frame, text="Avg Heart Rate:", fg="#ffffff", bg="#1f2937").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_workout_hr = tk.Entry(form_frame, width=10)
        self.entry_workout_hr.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        self.entry_workout_hr.insert(0, "110")

        tk.Label(form_frame, text="Workout Details:", fg="#ffffff", bg="#1f2937").grid(row=1, column=0, padx=5, pady=5, sticky="ne")
        self.txt_workout_details = tk.Text(form_frame, height=3, width=70, bg="#111827", fg="#ffffff", insertbackground="white", font=("Arial", 9))
        self.txt_workout_details.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="w")
        self.txt_workout_details.insert("1.0", "Leg Press 3x12 @ 180lbs, Treadmill Walk/Jog 15 mins")

        btn_log_workout = tk.Button(form_frame, text="Save Workout Log", bg="#10b981", fg="#ffffff", font=("Arial", 10, "bold"), command=self.log_workout)
        btn_log_workout.grid(row=2, column=1, columnspan=2, pady=5, sticky="w")

        # Dynamic exercise split reference label
        self.lbl_workout_helper = tk.Label(form_frame, text="Auto-Fill Details based on split", fg="#60a5fa", bg="#1f2937", font=("Arial", 9, "italic"))
        self.lbl_workout_helper.grid(row=2, column=3, columnspan=3, pady=5, sticky="e")
        self.combo_workout_type.bind("<<ComboboxSelected>>", self.on_workout_type_select)

        # Treeview to show past workouts
        past_lbl = tk.Label(left_frame, text="TRAINING LOG HISTORY", font=("Arial", 11, "bold"), fg="#ffffff", bg="#111827")
        past_lbl.pack(pady=10, anchor="w")

        cols = ("Date", "Type", "Duration", "Avg HR", "Details")
        self.workout_tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=8)
        self.workout_tree.pack(fill="both", expand=True)

        for col in cols:
            self.workout_tree.heading(col, text=col)
            self.workout_tree.column(col, width=90, anchor="center")
        self.workout_tree.column("Details", width=350, anchor="w")
        self.workout_tree.column("Type", width=180, anchor="w")

        tree_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.workout_tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.workout_tree.configure(yscrollcommand=tree_scroll.set)

        # RIGHT COLUMN: RECOVERY & SAFETY CHECK-IN
        tk.Label(right_frame, text="RECOVERY & SAFETY", font=("Arial", 12, "bold"), fg="#ffffff", bg="#1f2937").pack(pady=10)

        # Joint pain slider
        tk.Label(right_frame, text="Joint Pain Rating (1-10):", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.slider_joint_pain = tk.Scale(right_frame, from_=1, to=10, orient="horizontal", fg="#ffffff", bg="#1f2937", highlightthickness=0, activebackground="#3b82f6")
        self.slider_joint_pain.pack(fill="x", pady=2)
        self.slider_joint_pain.set(2)

        # DOMS soreness slider
        tk.Label(right_frame, text="Muscle Soreness (DOMS) (1-10):", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.slider_soreness = tk.Scale(right_frame, from_=1, to=10, orient="horizontal", fg="#ffffff", bg="#1f2937", highlightthickness=0, activebackground="#3b82f6")
        self.slider_soreness.pack(fill="x", pady=2)
        self.slider_soreness.set(2)

        # Sleep Quality slider
        tk.Label(right_frame, text="Sleep Quality (1-10):", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.slider_sleep = tk.Scale(right_frame, from_=1, to=10, orient="horizontal", fg="#ffffff", bg="#1f2937", highlightthickness=0, activebackground="#3b82f6")
        self.slider_sleep.pack(fill="x", pady=2)
        self.slider_sleep.set(7)

        # Weight entry
        tk.Label(right_frame, text="Body Weight (lbs):", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=2)
        self.entry_recovery_weight = tk.Entry(right_frame, width=35)
        self.entry_recovery_weight.pack(fill="x", pady=2)

        # Notes
        tk.Label(right_frame, text="Recovery Notes:", fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=5)
        self.entry_recovery_notes = tk.Entry(right_frame, width=35)
        self.entry_recovery_notes.pack(fill="x", pady=2)

        btn_save_recovery = tk.Button(right_frame, text="Save Daily Recovery Metrics", bg="#3b82f6", fg="#ffffff", font=("Arial", 9, "bold"), command=self.log_recovery)
        btn_save_recovery.pack(fill="x", pady=10)

        # Joint Safety Alert Card
        tk.Label(right_frame, text="JOINT SAFETY ALERT STATUS", font=("Arial", 10, "bold"), fg="#ffffff", bg="#1f2937").pack(anchor="w", pady=10)
        self.lbl_safety_warning = tk.Label(
            right_frame, 
            text="✅ Recovery Stable: Joint pain within safe training boundaries.\nProceed with scheduled Phase 1 workloads.",
            font=("Arial", 9, "bold"), 
            fg="#10b981", 
            bg="#111827", 
            padx=10, 
            pady=10,
            justify="left",
            wraplength=320
        )
        self.lbl_safety_warning.pack(fill="x", pady=5)

        self.load_workouts()
        self.load_recovery_logs()

    def on_workout_type_select(self, event):
        workout_type = self.combo_workout_type.get()
        self.txt_workout_details.delete("1.0", tk.END)

        if workout_type == "Lower Body & Joint Prep":
            self.txt_workout_details.insert("1.0", "Warm-up (5m joint mobility), Leg Press 3x12 @ 180lbs, Leg Extensions 3x12, Treadmill Walk/Jog progression 15m")
            self.lbl_workout_helper.config(text="Split: Tuesdays / Fridays")
        elif workout_type == "Upper Body & Calisthenics":
            self.txt_workout_details.insert("1.0", "Lat Pulldowns 3x10, Chest Press Machine 3x10, Assisted Dips/Pull-ups 3x8")
            self.lbl_workout_helper.config(text="Split: Wednesdays / Saturdays")
        elif workout_type == "YMCA Lap Swim":
            self.txt_workout_details.insert("1.0", "YMCA Lap Pool Swimming: 20 laps freestyle/breaststroke progression, low-impact cardio")
            self.lbl_workout_helper.config(text="Split: Wednesdays / Saturdays Swim")
        elif workout_type == "Light Mobility":
            self.txt_workout_details.insert("1.0", "Active Recovery stretching, joint decompression, thoracic mobility, light walking 15m")
            self.lbl_workout_helper.config(text="Split: Mon / Thu Wash Days")
        elif workout_type == "Rest & Recovery":
            self.txt_workout_details.insert("1.0", "No lifting or high impact cardio. Recovery focused, hydration baseline.")
            self.lbl_workout_helper.config(text="Split: Sundays")

    def log_workout(self):
        w_type = self.combo_workout_type.get()
        dur_str = self.entry_workout_dur.get().strip()
        hr_str = self.entry_workout_hr.get().strip()
        details = self.txt_workout_details.get("1.0", tk.END).strip()
        today = datetime.now().strftime("%Y-%m-%d")

        try:
            dur = int(dur_str)
            hr = int(hr_str)
        except ValueError:
            messagebox.showerror("Error", "Duration and Avg Heart Rate must be valid integers.")
            return

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workouts (date, workout_type, duration, avg_hr, details)
            VALUES (?, ?, ?, ?, ?)
        """, (today, w_type, dur, hr, details))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Workout logged successfully for {today}!")
        self.load_workouts()

    def log_recovery(self):
        pain = self.slider_joint_pain.get()
        soreness = self.slider_soreness.get()
        sleep = self.slider_sleep.get()
        weight_str = self.entry_recovery_weight.get().strip()
        notes = self.entry_recovery_notes.get().strip()
        today = datetime.now().strftime("%Y-%m-%d")

        weight = None
        if weight_str:
            try:
                weight = float(weight_str)
            except ValueError:
                messagebox.showerror("Error", "Weight must be a valid number.")
                return

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO recovery_logs (date, joint_pain, soreness, sleep_quality, weight_lbs, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (today, pain, soreness, sleep, weight, notes))

        if weight is not None:
            # Sync weight with baselines table
            cursor.execute("""
                UPDATE baselines 
                SET current_value = ? 
                WHERE marker_name = 'Weight'
            """, (weight,))
            # Save historical biometrics entry
            cursor.execute("""
                INSERT INTO biometrics_history (marker_name, recorded_value, recorded_date, notes)
                VALUES ('Weight', ?, ?, 'Logged via workouts & recovery check-in')
            """, (weight, today))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Recovery metrics saved for {today}!")
        self.load_recovery_logs()
        # Refresh baselines tab if open
        self.load_baselines()

    def load_workouts(self):
        for row in self.workout_tree.get_children():
            self.workout_tree.delete(row)

        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("SELECT date, workout_type, duration, avg_hr, details FROM workouts ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            self.workout_tree.insert("", "end", values=r)

    def load_recovery_logs(self):
        today = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("SELECT joint_pain, soreness, sleep_quality, notes, weight_lbs FROM recovery_logs WHERE date = ?", (today,))
        row = cursor.fetchone()
        
        # Also check last logged joint pain to update warning cards
        cursor.execute("SELECT joint_pain FROM recovery_logs ORDER BY date DESC LIMIT 1")
        last_pain_row = cursor.fetchone()
        conn.close()

        self.entry_recovery_weight.delete(0, tk.END)

        if row:
            self.slider_joint_pain.set(row[0])
            self.slider_soreness.set(row[1])
            self.slider_sleep.set(row[2])
            self.entry_recovery_notes.delete(0, tk.END)
            self.entry_recovery_notes.insert(0, row[3] if row[3] else "")
            if row[4] is not None:
                self.entry_recovery_weight.insert(0, str(row[4]))
        else:
            # Fallback default weight from baselines
            conn = sqlite3.connect("health_ops.db")
            cursor = conn.cursor()
            cursor.execute("SELECT current_value FROM baselines WHERE marker_name = 'Weight'")
            w_row = cursor.fetchone()
            conn.close()
            if w_row:
                self.entry_recovery_weight.insert(0, str(w_row[0]))

        # Evaluate safety warnings based on latest pain log
        if last_pain_row and last_pain_row[0] >= 7:
            self.lbl_safety_warning.config(
                text=f"⚠️ JOINT OVERLOAD WARNING (Pain: {last_pain_row[0]}/10):\n"
                     "High joint pain logged. Recommend skipping treadmill walk/jog progression. "
                     "Opt for YMCA lap swimming or active recovery mobility instead to protect tendons.",
                fg="#ef4444",
                bg="#7f1d1d"
            )
        else:
            self.lbl_safety_warning.config(
                text="✅ Recovery Stable: Joint pain within safe training boundaries.\n"
                     "Proceed with scheduled Phase 1 workloads.",
                fg="#10b981",
                bg="#064e3b"
            )

    def on_reconstitution_double_click(self, event):
        tree = event.widget
        selected = tree.selection()
        if not selected:
            return
        
        item_vals = tree.item(selected[0])['values']
        compound = item_vals[1] # Compound column
        
        # Switch notebook to the Re-order Planner tab (index 2)
        self.notebook.select(self.tab_orders)
        
        # Clear fields
        self.entry_item.delete(0, tk.END)
        self.entry_vials.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.entry_dose.delete(0, tk.END)
        self.entry_freq.delete(0, tk.END)
        
        self.entry_item.insert(0, compound)
        
        defaults_map = {
            "Tesamorelin": (10, 10.0, 25, 3),
            "Ipamorelin": (10, 10.0, 10, 3),
            "NAD+": (10, 500.0, 25, 3),
            "MOTS-c": (10, 10.0, 50, 1),
            "SS-31": (10, 10.0, 20, 3),
            "5-Amino-1MQ": (10, 50.0, 20, 3),
            "Semax": (10, 10.0, 10, 3),
            "Selank": (10, 10.0, 10, 3),
            "Pinealon": (10, 10.0, 20, 3),
            "DSIP": (10, 10.0, 10, 2),
            "KLOW Blend": (10, 80.0, 10, 3),
            "Glutathione": (10, 600.0, 50, 1),
            "Epithalon (Seasonal)": (10, 10.0, 20, 7),
            "Thymosin Alpha-1 (Seasonal)": (10, 10.0, 30, 3),
            "Lipo-C": (10, 10.0, 100, 3),
            "Vitamin B12": (10, 1.0, 50, 2),
            "BAC Water": (10, 10.0, 0, 0)
        }
        
        matched_key = None
        for k in defaults_map.keys():
            if k.lower() in compound.lower():
                matched_key = k
                break
                
        if matched_key:
            vials, size, dose, freq = defaults_map[matched_key]
        else:
            vials, size, dose, freq = 10, 10.0, 10, 3
            
        self.entry_vials.insert(0, str(vials))
        self.entry_size.insert(0, str(size))
        self.entry_dose.insert(0, str(dose))
        self.entry_freq.insert(0, str(freq))
        
        self.recalculate_reconstitution()

    def toggle_checklist_item(self, item, is_checked):
        today = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect("health_ops.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS checklist_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, item_text TEXT NOT NULL, checked INTEGER DEFAULT 0, UNIQUE(date, item_text))")
        cursor.execute("""
            INSERT OR REPLACE INTO checklist_logs (date, item_text, checked)
            VALUES (?, ?, ?)
        """, (today, item, 1 if is_checked else 0))
        conn.commit()
        conn.close()


    def show_master_poster(self):
        poster_win = tk.Toplevel(self.root)
        poster_win.title("AXL Master Protocol Phase 2 V7 Reference Poster")
        poster_win.geometry("1200x900")
        poster_win.configure(bg="#0b131f")

        poster_path = os.path.join("assets", "banners", "Hestia_Master_Protocol_V7.png")
        if not os.path.exists(poster_path):
            poster_path = os.path.join("Aergia_Web", "static", "assets", "banners", "Hestia_Banner.png")

        if os.path.exists(poster_path):
            from PIL import Image, ImageTk
            img = Image.open(poster_path)
            w_percent = 1150 / float(img.size[0])
            h_size = int(float(img.size[1]) * w_percent)
            resized_img = img.resize((1150, h_size), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)

            canvas = tk.Canvas(poster_win, bg="#0b131f", highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(poster_win, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)

            lbl = tk.Label(canvas, image=photo, bg="#0b131f")
            lbl.image = photo
            canvas.create_window((0, 0), window=lbl, anchor="nw")

            lbl.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            messagebox.showerror("Error", f"Poster image not found at {poster_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthOpsApp(root)
    root.mainloop()
