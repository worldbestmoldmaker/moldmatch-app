import streamlit as st
import pandas as pd

st.title("MoldMatch - Machine Selection Tool")

# ---------------------------
# MACHINE SELECTION (TOP UI)
# ---------------------------
st.header("Select Machine Brand")

col1, col2, col3, col4 = st.columns(4)

selected_oem = None

with col1:
    st.image("https://s3-prod.plasticsnews.com/styles/width_792/s3/ENGEL%20e-mac%20180.jpg")
    if st.button("ENGEL"):
        selected_oem = "ENGEL"

with col2:
    st.image("https://www.arburg.com/media/_processed_/b/f/csm_186074-ALLROUNDER-470H-PREMIUM_fc43cccff1.jpg")
    if st.button("ARBURG"):
        selected_oem = "ARBURG"

with col3:
    st.image("https://www.ptonline.com/products/high-speed-packaging-medical-demos-from-netstal")
    if st.button("NETSTAL"):
        selected_oem = "NETSTAL"

with col4:
    st.image("https://www.tkpm.eu/wp-content/uploads/2015/11/The-New-IntElect-5-2017.jpg")
    if st.button("SUMITOMO"):
        selected_oem = "SUMITOMO"


# Store selection
if "selected_oem" not in st.session_state:
    st.session_state.selected_oem = None

if selected_oem:
    st.session_state.selected_oem = selected_oem

if st.session_state.selected_oem:
    st.success(f"Selected OEM: {st.session_state.selected_oem}")

# ---------------------------
# INPUTS (MIDDLE)
# ---------------------------
st.header("Enter Mold Dimensions")

col1, col2, col3 = st.columns(3)

with col1:
    mold_length = st.number_input("Length (mm)", value=300)

with col2:
    mold_width = st.number_input("Width (mm)", value=300)

with col3:
    mold_height = st.number_input("Height / Thickness (mm)", value=400)

# Opening calculation
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

# ✅ OPTIONAL: filter by selected OEM
if st.session_state.selected_oem:
    df = df[df["OEM"] == st.session_state.selected_oem]

# ---------------------------
# CHECK FUNCTION
# ---------------------------
def check(machine):
    reasons = []

    # Width
    if machine["TieBar_X"] is not None:
        if mold_width > machine["TieBar_X"]:
            reasons.append("Too wide")
    else:
        if mold_width > machine["Platen_X"]:
            reasons.append("Too wide")

    # Length
    if machine["TieBar_Y"] is not None:
        if mold_length > machine["TieBar_Y"]:
            reasons.append("Too long")
    else:
        if mold_length > machine["Platen_Y"]:
            reasons.append("Too long")

    # Height / opening
    if required_opening > machine["Daylight"]:
        reasons.append("Insufficient daylight")

    return "PASS" if not reasons else "FAIL", ", ".join(reasons)

# ---------------------------
# RUN BUTTON (BOTTOM)
# ---------------------------
if st.button("Run Compatibility Check"):

    results = []

    for _, m in df.iterrows():
        status, reason = check(m)

        results.append({
            "OEM": m["OEM"],
            "Model": m["Model"],
            "Clamp (ton)": m["Clamp"],
            "Status": status,
            "Reason": reason
        })

    results_df = pd.DataFrame(results)

    st.subheader("Results")
    st.dataframe(results_df)

    # ---------------------------
    # BEST MACHINE
    # ---------------------------
    valid = results_df[results_df["Status"] == "PASS"]

    if len(valid) > 0:
        best = valid.sort_values("Clamp (ton)").iloc[0]

        st.success(
            f"✅ Recommended Machine:\n\n"
            f"{best['OEM']} - {best['Model']} ({best['Clamp (ton)']} ton)"
        )
    else:
        st.error("❌ No compatible machines found")