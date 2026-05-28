import streamlit as st

if st.button("Run Compatibility Check"):

    results = []

    for _, m in df.iterrows():
        status, reason = check(m)

        results.append({
            "OEM": m["OEM"],
            "Model": m["Model"],
            "Clamp": m["Clamp"],
            "Status": status,
            "Reason": reason
        })

    results_df = pd.DataFrame(results)

    st.subheader("Results")
    st.dataframe(results_df)

    # Recommendation
    valid = results_df[results_df["Status"] == "PASS"]

    if len(valid) > 0:
        best = valid.sort_values("Clamp").iloc[0]
        st.success(f"✅ Best Machine: {best['OEM']} {best['Model']} ({best['Clamp']} ton)")
    else:
        st.error("❌ No compatible machines")
