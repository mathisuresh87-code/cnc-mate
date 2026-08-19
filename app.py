import tkinter as tk
from tkinter import messagebox, ttk
import time

class MegalaCNCMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Megala CNC Mate - Smart Drawing & Animation Assistant")
        self.root.geometry("950x750")
        self.root.config(bg="#f0f2f5")

        # Header Title
        title_label = tk.Label(root, text="Megala CNC Mate - Auto Drawing Analyzer & Machining Simulator", 
                               font=("Arial", 14, "bold"), bg="#1e293b", fg="white", pady=10)
        title_label.pack(fill=tk.X)

        # Notebook for Multi-Tabs (Tab 1: Report, Tab 2: Animation)
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Setup Tabs
        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)

        notebook.add(self.tab1, text="  1. Dimensions & Report Generator  ")
        notebook.add(self.tab2, text="  2. Live Machining Animation Assistant  ")

        self.setup_tab1()
        self.setup_tab2()

    def setup_tab1(self):
        # Main Frame for Tab 1
        main_frame = tk.Frame(self.tab1, bg="#f0f2f5", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Section Frame
        input_frame = tk.LabelFrame(main_frame, text=" Enter Part Dimensions (Stepped Pin / Shaft) ", 
                                    font=("Arial", 11, "bold"), bg="white", fg="#334155", padx=10, pady=10)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Input Fields
        self.entries = {}
        fields = [
            ("Head Diameter (mm) [Ø]:", "18.0"),
            ("Head Thickness (mm):", "4.00"),
            ("Main Length (mm):", "35.0"),
            ("Tip / Tail Diameter (mm) [Ø]:", "7.06"),
            ("Overall Length (mm):", "38.70"),
            ("Cross Hole Diameter (mm) [Ø]:", "2.20"),
            ("Material Type:", "Free Cutting Steel / Brass")
        ]

        for i, (label_text, default_val) in enumerate(fields):
            lbl = tk.Label(input_frame, text=label_text, font=("Arial", 10), bg="white", anchor="w")
            lbl.grid(row=i, column=0, sticky="w", pady=5)
            
            ent = tk.Entry(input_frame, font=("Arial", 10), width=18)
            ent.insert(0, default_val)
            ent.grid(row=i, column=1, sticky="ew", pady=5)
            self.entries[label_text] = ent

        # Generate Button
        calc_btn = tk.Button(input_frame, text="Generate Machining Report", 
                             font=("Arial", 11, "bold"), bg="#2563eb", fg="white", 
                             command=self.generate_analysis, cursor="hand2", pady=8)
        calc_btn.grid(row=len(fields), column=0, columnspan=2, sticky="ew", pady=15)

        # Output Section Frame
        output_frame = tk.LabelFrame(main_frame, text=" Automated Machining Sequence & Guide ", 
                                     font=("Arial", 11, "bold"), bg="white", fg="#334155", padx=10, pady=10)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Text Box with Scrollbar for Output
        self.output_text = tk.Text(output_frame, font=("Courier New", 10), bg="#f8fafc", fg="#0f172a", wrap=tk.WORD)
        scrollbar = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.generate_analysis()

    def setup_tab2(self):
        # Animation Tab Setup
        anim_frame = tk.Frame(self.tab2, bg="#f0f2f5", padx=10, pady=10)
        anim_frame.pack(fill=tk.BOTH, expand=True)

        info_lbl = tk.Label(anim_frame, text="Visual Machining Simulation: See how the stepped pin is cut step-by-step!", 
                            font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#1e293b")
        info_lbl.pack(pady=5)

        # Canvas for Drawing & Animation
        self.canvas = tk.Canvas(anim_frame, width=850, height=400, bg="#0f172a")
        self.canvas.pack(pady=10)

        # Control Buttons
        btn_frame = tk.Frame(anim_frame, bg="#f0f2f5")
        btn_frame.pack(pady=10)

        start_anim_btn = tk.Button(btn_frame, text=" ▶ Play Machining Animation ", 
                                   font=("Arial", 11, "bold"), bg="#16a34a", fg="white", 
                                   command=self.run_animation, padx=15, pady=8, cursor="hand2")
        start_anim_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = tk.Button(btn_frame, text=" ↺ Reset View ", 
                              font=("Arial", 11, "bold"), bg="#dc2626", fg="white", 
                              command=self.draw_initial_stock, padx=15, pady=8, cursor="hand2")
        reset_btn.pack(side=tk.LEFT, padx=10)

        # Status Display Text
        self.status_lbl = tk.Label(anim_frame, text="Status: Ready to simulate. Click 'Play Machining Animation'.", 
                                   font=("Arial", 11, "italic"), bg="#f0f2f5", fg="#475569")
        self.status_lbl.pack(pady=5)

        # Draw initial view on load
        self.draw_initial_stock()

    def draw_initial_stock(self):
        self.canvas.delete("all")
        # Draw Raw Stock Bar (Big Cylinder)
        self.canvas.create_rectangle(150, 150, 750, 250, fill="#64748b", outline="#cbd5e1", width=2)
        self.canvas.text_stock = self.canvas.create_text(450, 130, text="Raw Material Bar Stock (Ø > 20mm)", fill="white", font=("Arial", 11, "bold"))
        self.status_lbl.config(text="Status: Raw material loaded. Ready for turning.")

    def run_animation(self):
        # Step 1: Facing & Turning Head
        self.status_lbl.config(text="Step 1: Facing & Turning Head Diameter (Ø18.0 mm)...")
        self.root.update()
        time.sleep(1)
        self.canvas.delete("all")
        
        # Draw Head
        self.canvas.create_rectangle(150, 160, 250, 240, fill="#38bdf8", outline="white", width=2)
        self.canvas.create_text(200, 135, text="Head (Ø18.0)", fill="#38bdf8", font=("Arial", 10, "bold"))
        
        # Remaining stock
        self.canvas.create_rectangle(250, 180, 750, 220, fill="#64748b", outline="#cbd5e1", width=2)
        self.root.update()
        time.sleep(1.2)

        # Step 2: Turning Main Body & Tip
        self.status_lbl.config(text="Step 2: Turning Main Body (35.0mm) & Tip (Ø7.06 mm)...")
        self.root.update()
        time.sleep(1)
        self.canvas.delete("all")

        # Head
        self.canvas.create_rectangle(150, 160, 250, 240, fill="#38bdf8", outline="white", width=2)
        self.canvas.create_text(200, 135, text="Head (Ø18.0)", fill="#38bdf8", font=("Arial", 10, "bold"))

        # Main Body
        self.canvas.create_rectangle(250, 175, 550, 225, fill="#38bdf8", outline="white", width=2)
        self.canvas.create_text(400, 150, text="Main Body (35.0 mm)", fill="#38bdf8", font=("Arial", 10, "bold"))

        # Tip Section
        self.canvas.create_rectangle(550, 190, 750, 210, fill="#38bdf8", outline="white", width=2)
        self.canvas.create_text(650, 165, text="Tip (Ø7.06)", fill="#38bdf8", font=("Arial", 10, "bold"))
        self.root.update()
        time.sleep(1.2)

        # Step 3: Cross Drilling
        self.status_lbl.config(text="Step 3: Cross-Drilling Ø2.20 mm Hole at the tip...")
        self.root.update()
        time.sleep(1)

        # Draw Cross Hole (Small Circle on Tip)
        self.canvas.create_oval(680, 196, 700, 204, fill="#ef4444", outline="yellow", width=2)
        self.canvas.create_text(690, 175, text="Cross Hole Ø2.20", fill="#ef4444", font=("Arial", 9, "bold"))
        
        self.status_lbl.config(text="Status: Machining Simulation Completed Successfully! 100% Ready.")

    def generate_analysis(self):
        try:
            head_dia = float(self.entries["Head Diameter (mm) [Ø]:"].get())
            head_thick = float(self.entries["Head Thickness (mm):"].get())
            main_len = float(self.entries["Main Length (mm):"].get())
            tip_dia = float(self.entries["Tip / Tail Diameter (mm) [Ø]:"].get())
            overall_len = float(self.entries["Overall Length (mm):"].get())
            cross_hole = float(self.entries["Cross Hole Diameter (mm) [Ø]:"].get())
            material = self.entries["Material Type:"].get()

            report = f"""==================================================
        MEGALA CNC MATE - PRODUCTION REPORT
==================================================
[1] RAW MATERIAL SELECTION:
    * Recommended Stock Bar Size: > Ø{head_dia + 2.0} mm
    * Selected Material: {material}

[2] MACHINING OPERATIONS SEQUENCE:
    -> STEP 1: FACING & CENTER DRILLING
       - Face the raw stock to clear surface.
       - Center drill for tailstock support if needed.

    -> STEP 2: TURNING HEAD & MAIN BODY
       - Turn outer diameter to Ø{head_dia} mm for a length of {head_thick} mm.
       - Step down and turn main body to length {main_len} mm.
       - Turn reduced tip section to Ø{tip_dia} mm.
       - Total Overall Length target: {overall_len} mm (Maintain 0 / -0.10 tolerance).

    -> STEP 3: CROSS-DRILLING OPERATION
       - Index spindle / Transfer to secondary milling setup.
       - Drill cross-hole of Ø{cross_hole} mm at specified position.
       - Apply 1.20 x 45° chamfer on hole edges to remove burrs.

[3] QUALITY & FINISHING NOTES (NOTE 1):
    * Ensure the component is 100% free from burrs, cracks, and dent marks.
    * Check dimensions with digital vernier / micrometer before parting off.

==================================================
   Status: Ready for Production & Visual Simulation!
==================================================
"""
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, report)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for dimensions!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MegalaCNCMateApp(root)
    root.mainloop()
