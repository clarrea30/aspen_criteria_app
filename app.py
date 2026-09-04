import streamlit as st

st.set_page_config(
    page_title="Pediatric ASPEN Malnutrition Assessment Tool",
    page_icon="🍎",
    layout="centered",
)

st.title("Pediatric ASPEN Malnutrition Assessment Tool")
st.markdown(
    "Based on the TCH Pediatric Malnutrition Tool / ASPEN consensus criteria. "
    "**Requires ≥ 2 indicators** to meet a severity tier."
)

# Helper function to estimate MUAC Z-score from raw cm, age, and sex
def estimate_muac_z(age_months, sex, muac_cm):
    if age_months < 6 or age_months > 60:
        return "Out of range (6-60 mo)"

    # Simplified WHO-based reference medians & SD approximations for demonstration
    base_median = 13.5 + (2.5 * (age_months / 60.0))
    if sex == "Female":
        base_median -= 0.2

    approx_sd = 1.2
    z_score = (muac_cm - base_median) / approx_sd

    if z_score <= -3.0:
        return "Severe (≤ -3)"
    elif -2.99 <= z_score <= -2.0:
        return "Moderate (-2 to -2.9)"
    elif -1.99 <= z_score <= -1.0:
        return "Mild (-1 to -1.9)"
    else:
        return "None / Normal"


with st.form("aspen_comprehensive_form"):
    st.subheader("1. Primary Anthropometric Indicators")

    col1, col2 = st.columns(2)
    with col1:
        wf_z = st.selectbox(
            "Wt-for-length or BMI-for-age Z-score",
            ["None / Normal", "Mild (-1 to -1.9)", "Moderate (-2 to -2.9)", "Severe (≤ -3)"],
        )
        ht_z = st.selectbox(
            "Length/Ht Z-score (Stunting)",
            ["None / Normal", "Moderate (-2 to -2.9)", "Severe (≤ -3)"],
        )

    with col2:
        muac_mode = st.radio(
            "MUAC Input Method", ["Select Z-score Tier", "Calculate from Raw (cm)"]
        )

        if muac_mode == "Select Z-score Tier":
            muac_z = st.selectbox(
                "MUAC Z-score",
                ["None / Normal", "Mild (-1 to -1.9)", "Moderate (-2 to -2.9)", "Severe (≤ -3)"],
            )
        else:
            st.markdown("Enter details for 6–60 month patient:")
            m_age = st.number_input("Age (months)", min_value=6, max_value=60, value=12)
            m_sex = st.selectbox("Sex", ["Male", "Female"])
            m_val = st.number_input(
                "Raw MUAC (cm)", min_value=8.0, max_value=25.0, value=14.0, step=0.1
            )
            muac_z = estimate_muac_z(m_age, m_sex, m_val)
            st.info(f"Calculated MUAC Category: **{muac_z}**")

    st.subheader("2. Secondary Indicators (Data Points & History)")
    st.markdown("Select any historical or functional indicators that apply:")

    wt_age_decline = st.selectbox(
        "Δ Weight-for-age / Growth Deceleration",
        [
            "None / Normal",
            "Decline in 1 Z-score (Mild)",
            "Decline in 2 Z-score (Moderate)",
            "Decline in 3 Z-score (Severe)",
        ],
    )

    wt_gain_velocity = st.selectbox(
        "Weight Gain Velocity / Expectation",
        [
            "None / Normal",
            "WHO growth velocity drop (-1 to -1.99 Z / <75% norm)",
            "WHO growth velocity drop (-2 to -2.9 Z / <50% norm)",
            "WHO growth velocity drop (-3 Z / <25% norm)",
        ],
    )

    wt_loss = st.selectbox(
        "Acute/Recent Weight Loss %",
        [
            "None / Normal",
            "5% usual body weight (Mild)",
            "7.5% usual body weight (Moderate)",
            "10% usual body weight (Severe)",
        ],
    )

    inadequate_intake = st.selectbox(
        "Inadequate Nutrient Intake Duration",
        [
            "Normal intake",
            "51-75% estimated energy/protein needs (Mild)",
            "26-50% estimated energy/protein needs (Moderate)",
            "≤25% estimated energy/protein needs (Severe)",
        ],
    )
    
    functional_capacity = st.selectbox(
        "Functional Capacity (for age)",
        [
            "No impairment",
            "Reduced ability to perform ADLs (Moderate)",
            "Significant reduced ability to perform ADLs/Bedbound (Severe)"
        ]
    )

    physical_assessment = st.selectbox(
        "Physical Assessment (Muscle or Fat Loss)",
        ["None / Normal", "Moderate loss", "Severe loss"],
    )

    submitted = st.form_submit_button("Evaluate ASPEN Criteria")


if submitted:
    mild_count = 0
    mod_count = 0
    sev_count = 0

    # Check primary indicators
    for val in [wf_z, ht_z, muac_z]:
        if "Mild" in str(val):
            mild_count += 1
        elif "Moderate" in str(val):
            mod_count += 1
        elif "Severe" in str(val):
            sev_count += 1

    # Check secondary indicators
    for val in [
        wt_age_decline,
        wt_gain_velocity,
        wt_loss,
        inadequate_intake,
        functional_capacity,
        physical_assessment,
    ]:
        if "Mild" in str(val):
            mild_count += 1
        elif "Moderate" in str(val):
            mod_count += 1
        elif "Severe" in str(val):
            sev_count += 1

    st.markdown("---")
    st.subheader("Evaluation Results")
    st.write(
        f"**Indicators Triggered:** {sev_count} Severe, {mod_count} Moderate, {mild_count} Mild"
    )

    # Final ASPEN evaluation logic (requires >= 2 indicators)
    if sev_count >= 2:
        st.error(
            "**Determination: SEVERE MALNUTRITION** (Met criteria with ≥ 2 severe indicators)"
        )
    elif mod_count >= 2 or (sev_count == 1 and mod_count >= 1):
        st.warning(
            "**Determination: MODERATE MALNUTRITION** (Met criteria with multiple moderate/severe indicators)"
        )
    elif mild_count >= 2 or mod_count == 1 or sev_count == 1:
        st.info(
            "**Determination: MILD MALNUTRITION** (Met criteria with multiple mild or single moderate/severe indicators)"
        )
    else:
        st.success(
            "**Determination: Well-Nourished / Does not meet threshold (< 2 qualifying indicators)**"
        )

    st.markdown(
        "*Note: This tool is intended to assist clinical judgment and should"
        " always be verified against official institutional guidelines and"
        " complete patient charting.*"
    )
