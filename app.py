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
