"""
╔══════════════════════════════════════════════════════╗
║       YATHIN'S PERSONALISED WORKOUT GENERATOR        ║
║                   Built with Python                  ║
╚══════════════════════════════════════════════════════╝
Run: python3 yathin_workout_generator.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import datetime

# ─── Workout Database ────────────────────────────────────────────────────────

WORKOUT_DB = {
    # Equipment → Exercise Types → Exercises (name, reps_unit, base_reps)
    "Treadmill": {
        "Cardio":   [("Sprint Intervals",    "mins", 20), ("Incline Walk",       "mins", 30),
                     ("Tempo Run",           "mins", 25), ("Recovery Jog",       "mins", 20)],
        "Stamina":  [("Long Distance Run",   "mins", 40), ("Endurance Walk",     "mins", 45),
                     ("Hill Repeats",        "rounds", 8)],
        "Balance":  [("Single-leg Treadmill Walk", "mins", 5)],
    },
    "Weights": {
        "Strength": [("Bicep Curls",         "reps", 12), ("Shoulder Press",     "reps", 10),
                     ("Deadlifts",           "reps", 8),  ("Bent-over Rows",     "reps", 10),
                     ("Tricep Extensions",   "reps", 12), ("Lateral Raises",     "reps", 15),
                     ("Goblet Squats",       "reps", 12), ("Romanian Deadlift",  "reps", 10)],
        "Stamina":  [("High-Rep Curls",      "reps", 20), ("Circuit Training",   "rounds", 5)],
        "Cardio":   [("Dumbbell Thrusters",  "reps", 15), ("Dumbbell Swings",    "reps", 20)],
    },
    "Bike": {
        "Cardio":   [("Sprint Cycling",      "mins", 20), ("Steady State Ride",  "mins", 30),
                     ("Interval Cycling",    "rounds", 8)],
        "Stamina":  [("Long Ride",           "mins", 45), ("Hill Climb Sim",     "mins", 25)],
        "Strength": [("Resistance Climb",    "mins", 15), ("High-Resistance Sprint", "rounds", 6)],
    },
    "Yoga Ball": {
        "Balance":      [("Ball Plank Hold",     "secs", 30), ("Seated Balance",     "mins", 3),
                         ("Wall Ball Squat",     "reps", 15), ("Ball Toss Balance",  "reps", 20)],
        "Flexibility":  [("Spine Stretch",       "secs", 45), ("Hip Flexor Roll",    "secs", 60),
                         ("Chest Opener",        "secs", 30), ("Hamstring Roll",     "reps", 12)],
        "Strength":     [("Ball Push-up",        "reps", 12), ("Ball Pike",          "reps", 10),
                         ("Ball Pass",           "reps", 15)],
    },
    "Pull Up Bar": {
        "Strength": [("Pull-ups",            "reps", 8),  ("Chin-ups",          "reps", 8),
                     ("Hanging Knee Raises", "reps", 15), ("Wide Grip Pull-up",  "reps", 6),
                     ("Commando Pull-ups",   "reps", 8)],
        "Stamina":  [("Dead Hang",           "secs", 30), ("Scapular Pull-ups",  "reps", 15)],
        "Balance":  [("L-sit Hold",          "secs", 20), ("Tuck Hold",          "secs", 15)],
    },
}

ALL_EXERCISE_TYPES = ["Cardio", "Strength", "Flexibility", "Balance", "Stamina"]

COLORS = {
    "bg":           "#0D0F14",
    "panel":        "#151820",
    "card":         "#1C2030",
    "accent1":      "#FF4D6D",   # hot pink-red
    "accent2":      "#00D9FF",   # cyan
    "accent3":      "#FFD600",   # yellow
    "text":         "#F0F4FF",
    "muted":        "#6B7080",
    "border":       "#252A3A",
    "check_on":     "#00D9FF",
    "check_off":    "#252A3A",
    "btn":          "#FF4D6D",
    "btn_hover":    "#FF2050",
    "success":      "#00E5A0",
}

EQUIP_ICONS = {
    "Treadmill":   "🏃",
    "Weights":     "🏋️",
    "Bike":        "🚴",
    "Yoga Ball":   "⚽",
    "Pull Up Bar": "🔝",
}

TYPE_ICONS = {
    "Cardio":      "❤️",
    "Strength":    "💪",
    "Flexibility": "🧘",
    "Balance":     "⚖️",
    "Stamina":     "⚡",
}

# ─── Main Application ─────────────────────────────────────────────────────────

class WorkoutApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yathin's Workout Generator")
        self.configure(bg=COLORS["bg"])
        self.geometry("960x780")
        self.minsize(860, 700)
        self.resizable(True, True)

        self._equip_vars  = {}
        self._type_vars   = {}
        self._reps_var    = tk.IntVar(value=3)
        self._result_text = tk.StringVar()

        self._setup_fonts()
        self._build_ui()
        self.center_window()

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _setup_fonts(self):
        self.f_title   = font.Font(family="Courier New", size=22, weight="bold")
        self.f_sub     = font.Font(family="Courier New", size=10)
        self.f_section = font.Font(family="Courier New", size=13, weight="bold")
        self.f_label   = font.Font(family="Courier New", size=11)
        self.f_small   = font.Font(family="Courier New", size=9)
        self.f_btn     = font.Font(family="Courier New", size=13, weight="bold")
        self.f_result  = font.Font(family="Courier New", size=11)
        self.f_result_h= font.Font(family="Courier New", size=13, weight="bold")

    def center_window(self):
        self.update_idletasks()
        w, h = 960, 780
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI Builder ────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self, bg=COLORS["bg"], pady=18)
        hdr.pack(fill="x", padx=30)

        tk.Label(hdr, text="YATHIN'S", font=self.f_sub,
                 bg=COLORS["bg"], fg=COLORS["accent2"]).pack(anchor="w")
        tk.Label(hdr, text="WORKOUT GENERATOR", font=self.f_title,
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(hdr, text="Select your gear · Choose your goals · Set your reps",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["muted"]).pack(anchor="w")

        sep = tk.Frame(self, bg=COLORS["accent1"], height=2)
        sep.pack(fill="x", padx=30, pady=(0, 10))

        # ── Scroll Canvas ──
        canvas = tk.Canvas(self, bg=COLORS["bg"], highlightthickness=0)
        vsb    = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True, padx=(30, 0))

        inner = tk.Frame(canvas, bg=COLORS["bg"])
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_resize(e):
            canvas.itemconfig(win_id, width=e.width)

        inner.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>",   lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>",   lambda e: canvas.yview_scroll( 1, "units"))

        # ── Three-Column Row: Equipment | Exercise Types | Reps ──
        row = tk.Frame(inner, bg=COLORS["bg"])
        row.pack(fill="x", pady=(0, 14))

        self._build_equipment_panel(row)
        self._build_type_panel(row)
        self._build_reps_panel(row)

        # ── Generate Button ──
        btn_frame = tk.Frame(inner, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=(6, 16))

        self._gen_btn = tk.Button(
            btn_frame,
            text="⚡  GENERATE MY WORKOUT",
            font=self.f_btn,
            bg=COLORS["accent1"], fg=COLORS["text"],
            activebackground=COLORS["btn_hover"], activeforeground=COLORS["text"],
            relief="flat", cursor="hand2", padx=30, pady=14,
            command=self._generate
        )
        self._gen_btn.pack(side="left")

        clr_btn = tk.Button(
            btn_frame,
            text="↺  RESET",
            font=self.f_small,
            bg=COLORS["card"], fg=COLORS["muted"],
            activebackground=COLORS["border"], activeforeground=COLORS["text"],
            relief="flat", cursor="hand2", padx=18, pady=14,
            command=self._reset
        )
        clr_btn.pack(side="left", padx=(12, 0))

        # ── Result Area ──
        self._result_frame = tk.Frame(inner, bg=COLORS["bg"])
        self._result_frame.pack(fill="both", expand=True, pady=(0, 30))

    def _panel(self, parent, title, color_accent, **kwargs):
        """Creates a styled card panel."""
        outer = tk.Frame(parent, bg=COLORS["border"], padx=1, pady=1, **kwargs)
        outer.pack(side="left", fill="both", expand=True, padx=(0, 14), pady=0)

        card = tk.Frame(outer, bg=COLORS["card"], padx=18, pady=16)
        card.pack(fill="both", expand=True)

        stripe = tk.Frame(card, bg=color_accent, height=3)
        stripe.pack(fill="x", pady=(0, 10))

        tk.Label(card, text=title, font=self.f_section,
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 10))

        return card

    def _checkbox(self, parent, label, var, icon=""):
        """Custom styled checkbox row."""
        row = tk.Frame(parent, bg=COLORS["card"], pady=3)
        row.pack(fill="x")

        indicator = tk.Label(row, text="◉", font=self.f_label,
                             bg=COLORS["card"], fg=COLORS["check_off"],
                             cursor="hand2", width=2)
        indicator.pack(side="left")

        lbl = tk.Label(row, text=f"{icon} {label}" if icon else label,
                       font=self.f_label, bg=COLORS["card"],
                       fg=COLORS["muted"], cursor="hand2", anchor="w")
        lbl.pack(side="left", fill="x", expand=True)

        def toggle(*_):
            var.set(not var.get())
            _update()

        def _update():
            if var.get():
                indicator.config(fg=COLORS["check_on"])
                lbl.config(fg=COLORS["text"])
            else:
                indicator.config(fg=COLORS["check_off"])
                lbl.config(fg=COLORS["muted"])

        indicator.bind("<Button-1>", toggle)
        lbl.bind("<Button-1>", toggle)
        row.bind("<Button-1>", toggle)

        _update()
        return row

    def _build_equipment_panel(self, parent):
        card = self._panel(parent, "⚙  EQUIPMENT", COLORS["accent2"])
        tk.Label(card, text="What do you have available?",
                 font=self.f_small, bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w", pady=(0, 8))

        for equip in ["Treadmill", "Weights", "Bike", "Yoga Ball", "Pull Up Bar"]:
            var = tk.BooleanVar(value=False)
            self._equip_vars[equip] = var
            self._checkbox(card, equip, var, icon=EQUIP_ICONS[equip])

        # Select All
        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=(10, 6))
        all_btn = tk.Button(card, text="Select All", font=self.f_small,
                            bg=COLORS["bg"], fg=COLORS["accent2"],
                            activebackground=COLORS["border"], relief="flat",
                            cursor="hand2", pady=4,
                            command=lambda: [v.set(True) or self._refresh_checks()
                                             for v in self._equip_vars.values()])
        all_btn.pack(anchor="w")

    def _build_type_panel(self, parent):
        card = self._panel(parent, "🎯  EXERCISE TYPES", COLORS["accent1"])
        tk.Label(card, text="What kind of training?",
                 font=self.f_small, bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w", pady=(0, 8))

        for etype in ALL_EXERCISE_TYPES:
            var = tk.BooleanVar(value=False)
            self._type_vars[etype] = var
            self._checkbox(card, etype, var, icon=TYPE_ICONS[etype])

        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=(10, 6))
        all_btn = tk.Button(card, text="Select All", font=self.f_small,
                            bg=COLORS["bg"], fg=COLORS["accent1"],
                            activebackground=COLORS["border"], relief="flat",
                            cursor="hand2", pady=4,
                            command=lambda: [v.set(True) or self._refresh_checks()
                                             for v in self._type_vars.values()])
        all_btn.pack(anchor="w")

    def _build_reps_panel(self, parent):
        card = self._panel(parent, "🔢  SETS & REPS", COLORS["accent3"])
        tk.Label(card, text="How many sets per exercise?",
                 font=self.f_small, bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w", pady=(0, 8))

        # Live value label
        self._reps_label = tk.Label(card, text="3 SETS", font=self.f_section,
                                     bg=COLORS["card"], fg=COLORS["accent3"])
        self._reps_label.pack(anchor="w", pady=(4, 10))

        slider = tk.Scale(
            card,
            from_=1, to=10,
            orient="horizontal",
            variable=self._reps_var,
            command=self._on_slider,
            bg=COLORS["card"], fg=COLORS["text"],
            troughcolor=COLORS["border"],
            activebackground=COLORS["accent3"],
            highlightthickness=0,
            sliderlength=22,
            length=160,
            showvalue=False,
            font=self.f_small,
        )
        slider.pack(fill="x", pady=(0, 6))

        # Tick labels
        tick_frame = tk.Frame(card, bg=COLORS["card"])
        tick_frame.pack(fill="x")
        for n in [1, 3, 5, 7, 10]:
            tk.Label(tick_frame, text=str(n), font=self.f_small,
                     bg=COLORS["card"], fg=COLORS["muted"]).pack(side="left", expand=True)

        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=(14, 8))

        # Intensity display
        tk.Label(card, text="INTENSITY LEVEL", font=self.f_small,
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")
        self._intensity_label = tk.Label(card, text="◆◆◆◇◇  MODERATE",
                                          font=self.f_small, bg=COLORS["card"],
                                          fg=COLORS["accent3"])
        self._intensity_label.pack(anchor="w", pady=(4, 0))
        self._update_intensity()

    # ── Interaction ───────────────────────────────────────────────────────────

    def _refresh_checks(self):
        """Force UI refresh after bulk set."""
        self.update_idletasks()

    def _on_slider(self, val):
        n = int(float(val))
        self._reps_label.config(text=f"{n} SET{'S' if n > 1 else ''}")
        self._update_intensity()

    def _update_intensity(self):
        n = self._reps_var.get()
        if n <= 2:
            label, dots = "EASY",     "◆◇◇◇◇"
        elif n <= 4:
            label, dots = "MODERATE", "◆◆◆◇◇"
        elif n <= 6:
            label, dots = "HARD",     "◆◆◆◆◇"
        elif n <= 8:
            label, dots = "INTENSE",  "◆◆◆◆◆"
        else:
            label, dots = "BEAST MODE","◆◆◆◆◆+"
        self._intensity_label.config(text=f"{dots}  {label}")

    def _reset(self):
        for v in self._equip_vars.values(): v.set(False)
        for v in self._type_vars.values():  v.set(False)
        self._reps_var.set(3)
        self._reps_label.config(text="3 SETS")
        self._update_intensity()
        for w in self._result_frame.winfo_children():
            w.destroy()

    # ── Generator ─────────────────────────────────────────────────────────────

    def _generate(self):
        selected_equip = [e for e, v in self._equip_vars.items() if v.get()]
        selected_types = [t for t, v in self._type_vars.items()  if v.get()]
        sets           = self._reps_var.get()

        if not selected_equip:
            messagebox.showwarning("No Equipment", "Please select at least one piece of equipment! 💪")
            return
        if not selected_types:
            messagebox.showwarning("No Exercise Type", "Please select at least one exercise type! 🎯")
            return

        # Build workout plan
        plan = []  # list of (equip, type, exercise_name, reps, unit)
        for equip in selected_equip:
            for etype in selected_types:
                options = WORKOUT_DB.get(equip, {}).get(etype, [])
                if options:
                    ex_name, unit, base = random.choice(options)
                    # Scale reps by set count
                    reps = max(1, round(base * (0.7 + sets * 0.06)))
                    plan.append((equip, etype, ex_name, reps, unit))

        if not plan:
            messagebox.showinfo("No Matches",
                "No exercises found for that combination.\nTry different equipment or exercise types!")
            return

        random.shuffle(plan)
        self._render_result(plan, sets, selected_equip, selected_types)

    def _render_result(self, plan, sets, equip_list, type_list):
        # Clear old results
        for w in self._result_frame.winfo_children():
            w.destroy()

        now  = datetime.datetime.now().strftime("%d %b %Y · %H:%M")
        mins = len(plan) * sets * 3 // 2

        # ─ Result Header Card ─
        hdr = tk.Frame(self._result_frame, bg=COLORS["card"], padx=20, pady=16)
        hdr.pack(fill="x", pady=(0, 12))

        stripe = tk.Frame(hdr, bg=COLORS["success"], height=3)
        stripe.pack(fill="x", pady=(0, 12))

        top = tk.Frame(hdr, bg=COLORS["card"])
        top.pack(fill="x")

        tk.Label(top, text="✅  YOUR WORKOUT IS READY!",
                 font=self.f_result_h, bg=COLORS["card"], fg=COLORS["success"]).pack(side="left")
        tk.Label(top, text=now, font=self.f_small,
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(side="right")

        stats = tk.Frame(hdr, bg=COLORS["card"])
        stats.pack(fill="x", pady=(10, 0))

        for label, val in [
            ("EXERCISES", str(len(plan))),
            ("SETS EACH",  str(sets)),
            ("EST. TIME",  f"~{mins} mins"),
            ("EQUIPMENT",  str(len(equip_list))),
        ]:
            box = tk.Frame(stats, bg=COLORS["bg"], padx=12, pady=8)
            box.pack(side="left", padx=(0, 8))
            tk.Label(box, text=val,   font=self.f_result_h, bg=COLORS["bg"], fg=COLORS["accent2"]).pack()
            tk.Label(box, text=label, font=self.f_small,    bg=COLORS["bg"], fg=COLORS["muted"]).pack()

        # ─ Exercise Cards ─
        for i, (equip, etype, name, reps, unit) in enumerate(plan, 1):
            self._exercise_card(self._result_frame, i, equip, etype, name, reps, unit, sets)

        # ─ Footer ─
        footer = tk.Frame(self._result_frame, bg=COLORS["card"], padx=20, pady=10)
        footer.pack(fill="x", pady=(8, 0))
        tk.Label(footer,
                 text=f"💡  Remember to warm up before and cool down after your session. Stay hydrated, Yathin! 🔥",
                 font=self.f_small, bg=COLORS["card"], fg=COLORS["muted"],
                 wraplength=800, justify="left").pack(anchor="w")

    def _exercise_card(self, parent, idx, equip, etype, name, reps, unit, sets):
        # type colour
        type_colors = {
            "Cardio":      COLORS["accent1"],
            "Strength":    COLORS["accent2"],
            "Flexibility": COLORS["success"],
            "Balance":     COLORS["accent3"],
            "Stamina":     "#CC88FF",
        }
        col = type_colors.get(etype, COLORS["muted"])

        outer = tk.Frame(parent, bg=col, padx=1, pady=1)
        outer.pack(fill="x", pady=(0, 8))

        card = tk.Frame(outer, bg=COLORS["panel"], padx=16, pady=12)
        card.pack(fill="x")

        # Left: number + info
        left = tk.Frame(card, bg=COLORS["panel"])
        left.pack(side="left", fill="both", expand=True)

        num_lbl = tk.Label(left, text=f"{idx:02d}", font=self.f_section,
                           bg=COLORS["panel"], fg=col)
        num_lbl.pack(side="left", padx=(0, 12))

        info = tk.Frame(left, bg=COLORS["panel"])
        info.pack(side="left", fill="both", expand=True)

        tk.Label(info, text=name, font=self.f_result_h,
                 bg=COLORS["panel"], fg=COLORS["text"]).pack(anchor="w")

        tags = tk.Frame(info, bg=COLORS["panel"])
        tags.pack(anchor="w", pady=(4, 0))

        for tag_text, tag_col in [
            (f"{TYPE_ICONS.get(etype,'')} {etype}", col),
            (f"{EQUIP_ICONS.get(equip,'')} {equip}", COLORS["muted"]),
        ]:
            t = tk.Label(tags, text=tag_text, font=self.f_small,
                         bg=COLORS["bg"], fg=tag_col, padx=6, pady=2)
            t.pack(side="left", padx=(0, 6))

        # Right: reps info
        right = tk.Frame(card, bg=COLORS["panel"])
        right.pack(side="right")

        tk.Label(right, text=f"{reps}", font=font.Font(family="Courier New", size=24, weight="bold"),
                 bg=COLORS["panel"], fg=col).pack(anchor="e")
        tk.Label(right, text=f"{unit}  ×  {sets} sets", font=self.f_small,
                 bg=COLORS["panel"], fg=COLORS["muted"]).pack(anchor="e")

        # Completed checkbox
        done_var = tk.BooleanVar(value=False)
        done_lbl = tk.Label(right, text="☐  Mark done", font=self.f_small,
                            bg=COLORS["panel"], fg=COLORS["muted"], cursor="hand2")
        done_lbl.pack(anchor="e", pady=(6, 0))

        def toggle_done(_, lbl=done_lbl, v=done_var, c=card):
            v.set(not v.get())
            if v.get():
                lbl.config(text="☑  Completed!", fg=COLORS["success"])
                c.config(bg="#1a2220")
            else:
                lbl.config(text="☐  Mark done", fg=COLORS["muted"])
                c.config(bg=COLORS["panel"])

        done_lbl.bind("<Button-1>", toggle_done)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = WorkoutApp()
    app.mainloop()
