import streamlit as st
import pandas as pd

# ✅ Step 1: Define machine data FIRST
machines = [
    {"OEM": "NETSTAL", "Model": "ELION 800", "Clamp": 85,
     "Platen_X": 600, "Platen_Y": 550,
     "TieBar_X": 380, "TieBar_Y": 380,
     "Daylight": 650},

    {"OEM": "ARBURG", "Model": "470 A 1300-400", "Clamp": 400,
     "Platen_X": 900, "Platen_Y": 900,
     "TieBar_X": 600, "TieBar_Y": 600,
     "Daylight": 1100},
]

# ✅ Step 2: Create dataframe BEFORE using it
df = pd.DataFrame(machines)

# ✅ Step 3: THEN use it
if st.button("Run Compatibility Check"):

    for _, m in df.iterrows():
        st.write(m["Model"])