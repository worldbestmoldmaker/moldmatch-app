import pandas as pd

# ---------------------------
# MACHINE DATABASE (sample)
# ---------------------------
machines = [
    {"OEM": "NETSTAL", "Model": "ELION 800", "Clamp": 85,
     "Platen_X": 600, "Platen_Y": 550,
     "TieBar_X": 380, "TieBar_Y": 380,
     "Daylight": 650},

    {"OEM": "ARBURG", "Model": "470 A 1300-400", "Clamp": 400,
     "Platen_X": 900, "Platen_Y": 900,
     "TieBar_X": 600, "TieBar_Y": 600,
     "Daylight": 1100},

    {"OEM": "SUMITOMO", "Model": "SE180EV-A", "Clamp": 198,
     "Platen_X": 830, "Platen_Y": 760,
     "TieBar_X": 560, "TieBar_Y": 560,
     "Daylight": 900},

    {"OEM": "ENGEL", "Model": "e-victory 170/100", "Clamp": 100,
     "Platen_X": 650, "Platen_Y": 600,
     "TieBar_X": None, "TieBar_Y": None,  # tie-barless
     "Daylight": 800},
]

df = pd.DataFrame(machines)

# ---------------------------
# USER INPUT (MOLD DATA)
# ---------------------------
mold_width = float(input("Enter mold width (mm): "))
mold_height = float(input("Enter mold height (mm): "))
mold_thickness = float(input("Enter mold thickness (mm): "))
safety_clearance = 20  # mm (standard)

required_opening = mold_thickness + safety_clearance

# ---------------------------
# VALIDATION FUNCTION
# ---------------------------
def check_machine(machine):
    reasons = []
    
    # Width check
    if machine["TieBar_X"] is not None:
        if mold_width > machine["TieBar_X"]:
            reasons.append("Too wide for tie bars")
    else:
        if mold_width > machine["Platen_X"]:
            reasons.append("Too wide for platen")
    
    # Height check
    if machine["TieBar_Y"] is not None:
        if mold_height > machine["TieBar_Y"]:
            reasons.append("Too tall for tie bars")
    else:
        if mold_height > machine["Platen_Y"]:
            reasons.append("Too tall for platen")

    # Opening check
    if required_opening > machine["Daylight"]:
        reasons.append("Insufficient daylight")

    if len(reasons) == 0:
        return "PASS", []
    else:
        return "FAIL", reasons

# ---------------------------
# RUN ANALYSIS
# ---------------------------
results = []

for _, machine in df.iterrows():
    status, reasons = check_machine(machine)
    
    results.append({
        "Model": machine["Model"],
        "OEM": machine["OEM"],
        "Clamp (ton)": machine["Clamp"],
        "Status": status,
        "Reasons": ", ".join(reasons)
    })

results_df = pd.DataFrame(results)

# Show results
print("\n=== MACHINE COMPATIBILITY ===")
print(results_df)

# ---------------------------
# MACHINE RECOMMENDER
# ---------------------------
valid_machines = results_df[results_df["Status"] == "PASS"]

if len(valid_machines) > 0:
    best = valid_machines.sort_values("Clamp (ton)").iloc[0]
    
    print("\n⭐ RECOMMENDED MACHINE:")
    print(f"{best['OEM']} - {best['Model']} ({best['Clamp (ton)']} ton)")
else:
    print("\n❌ No compatible machines found.")

