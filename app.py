import streamlit as st
import pandas as pd

st.title("MoldMatch - Machine Compatibility Tool")

# ---------------------------
# INPUTS (L, W, H)
# ---------------------------
st.header("Enter Mold Dimensions")

col1, col2, col3 = st.columns(3)

with col1:
    mold_length = st.number_input("Length (mm)", value=300)

with col2:
    mold_width = st.number_input("Width (mm)", value=300)

with col3:
    mold_height = st.number_input("Height / Thickness (mm)", value=400)

# Opening requirement
safety_clearance = 20
required_opening = mold_height + safety_clearance

st.info(f"Required Machine Opening: {required_opening} mm")

# ---------------------------
# MACHINE DATABASE
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
     "TieBar_X": None, "TieBar_Y": None,
     "Daylight": 800},
]

df = pd.DataFrame(machines)

# ---------------------------
# CHECK FUNCTION
# ---------------------------
def check_machine(machine):
    reasons = []

    # WIDTH check (X direction)
    if machine["TieBar_X"] is not None:
        if mold_width > machine["TieBar_X"]:
            reasons.append("Too wide for tie bars")
    else:
        if mold_width > machine["Platen_X"]:
            reasons.append("Too wide for platen")

    # LENGTH check (Y direction)
    if machine["TieBar_Y"] is not None:
        if mold_length > machine["TieBar_Y"]:
            reasons.append("Too long for tie bars")
    else:
        if mold_length > machine["Platen_Y"]:
            reasons.append("Too long for platen")

    # HEIGHT / OPENING check
    if required_opening > machine["Daylight"]:
        reasons.append("Insufficient daylight")

    if len(reasons) == 0:
        return "PASS", ""
    else:
        return "FAIL", ", ".join(reasons)

# ---------------------------
# RUN BUTTON
# ---------------------------
if st.button("Run Compatibility Check"):

    results = []

    for _, m in df.iterrows():
        status, reason = check_machine(m)

        results.append({
            "OEM": m["OEM"],
            "Model": m["Model"],
            "Clamp (ton)": m["Clamp"],
            "Status": status,
            "Reason": reason
        })

    results_df = pd.DataFrame(results)

    # Show results
    st.subheader("Compatibility Results")
    st.dataframe(results_df)

    # ---------------------------
    # BEST MACHINE SELECTION
    # ---------------------------
    valid = results_df[results_df["Status"] == "PASS"]

    if len(valid) > 0:
        # Choose smallest clamp machine → efficient choice
        best = valid.sort_values("Clamp (ton)").iloc[0]

        st.success(
            f"✅ Recommended Machine:\n\n"
            f"{best['OEM']} - {best['Model']} ({best['Clamp (ton)']} ton)"
        )
    else:
        st.error("❌ No compatible machines found")
