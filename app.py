import streamlit as st

st.set_page_config(
    page_title="Pediatric ASPEN Malnutrition Calculator", page_icon="🍎", layout="centered"
)

st.title("Pediatric ASPEN Malnutrition Calculator")
st.markdown(
    "A decision-support tool based on ASPEN/Academy consensus clinical characteristics for pediatric malnutrition."
)

with st.form("aspen_form"):
  st.subheader("1. Clinical Context & Etiology")
  etiology = st.selectbox(
      "Select Clinical Condition Type",
      [
          "Select...",
          "Acute Illness or Injury (e.g., trauma, burns, surgery)",
          "Chronic Condition (e.g., organ failure, cerebral palsy, prematurity)",
          "Environmental / Social (e.g., neglect, poverty)",
      ],
  )

  st.subheader("2. Anthropometric Indicators (Z-scores / Growth Data)")
  st.markdown(
      "Enter the patient's most applicable compromised metric (choose the"
      " worst category if multiple apply)."
  )

  weight_for_length_bmi = st.selectbox(
      "Weight-for-length / BMI-for-age / MUAC Z-score",
      [
          "Normal (≥ -1.0)",
          "Mild (-1.1 to -1.9)",
          "Moderate (-2.0 to -2.9)",
          "Severe (≤ -3.0)",
      ],
  )

  height_for_age = st.selectbox(
      "Length/Height-for-age Z-Score (Chronic indicator)",
      [
          "Normal (≥ -1.0)",
          "Mild (-1.1 to -1.9)",
          "Moderate (-2.0 to -2.9)",
          "Severe (≤ -3.0)",
      ],
  )

  st.subheader("3. Historical / Velocity & Intake Indicators")

  # Dynamic guidance based on acute vs chronic
  if "Acute" in etiology:
    weight_velocity = st.selectbox(
        "Weight Deceleration / Loss (Acute)",
        [
            "None / Normal",
            "Not applicable or unknown",
            (
                "W/L z-score drop of 1 z-score (or % weight loss across time"
                " depending on age)"
            ),
            (
                "Inadvisable weight gain / crossing 2 major height/weight"
                " percentiles (infants)"
            ),
        ],
    )
    intake_duration = st.selectbox(
        "Inadequate Energy Intake Duration",
        [
            "Normal intake",
            "≤ 75% estimated energy requirement for ≥ 1 week",
            "≤ 50% estimated energy requirement for ≥ 2 weeks",
            "≤ 75% estimated energy requirement for ≥ 1 month",
            "≤ 50% estimated energy requirement for ≥ 1 month",
            "≤ 25% estimated energy requirement for ≥ 1 week",
        ],
    )
  elif "Chronic" in etiology or "Environmental" in etiology:
    weight_velocity = st.selectbox(
        "Rate of Weight Loss / Growth Deceleration (Chronic/Environmental)",
        [
            "None / Normal",
            "Deceleration in weight gain across 2 major percentile positions",
            "Inadequate weight gain over time",
        ],
    )
    intake_duration = st.selectbox(
        "Inadequate Energy Intake Duration (Chronic/Environmental)",
        [
            "Normal intake",
            "≤ 75% estimated energy requirement for ≥ 1 month",
            "≤ 50-75% estimated energy requirement for ≥ 2-3 months",
            "≤ 50% estimated energy requirement for ≥ 1 month",
        ],
    )
  else:
    weight_velocity = "None / Normal"
    intake_duration = "Normal intake"

  submitted = st.form_submit_button("Calculate ASPEN Classification")

# Logic Evaluation upon submission
if submitted:
  if etiology == "Select...":
    st.error("Please select a valid clinical condition type (Etiology).")
  else:
    # Diagnostic decision logic evaluation
    severity = "No Malnutrition / Well-Nourished"

    # Evaluate based on standard ASPEN cutoffs embedded in selections
    if "Severe" in weight_for_length_bmi or "Severe" in height_for_age:
      severity = "Severe Malnutrition"
    elif "Moderate" in weight_for_length_bmi or "Moderate" in height_for_age:
      severity = "Moderate Malnutrition"
    elif "Mild" in weight_for_length_bmi or "Mild" in height_for_age:
      severity = "Mild Malnutrition"
    elif "1 z-score" in weight_velocity or "2 major percentile" in weight_velocity:
      if "Acute" in etiology:
        severity = "Moderate Malnutrition"
      else:
        severity = "Mild to Moderate Malnutrition (Check intake/duration)"
    elif (
        "50%" in intake_duration
        or "25%" in intake_duration
        or "1 month" in intake_duration
    ):
      severity = "Moderate to Severe Malnutrition (Review full metrics)"
    elif "75%" in intake_duration:
      severity = "Mild Malnutrition"

    st.markdown("---")
    st.subheader("Diagnostic Result")
    if "Severe" in severity:
      st.error(f"**Classification:** {severity} ({etiology})")
    elif "Moderate" in severity:
      st.warning(f"**Classification:** {severity} ({etiology})")
    elif "Mild" in severity:
      st.info(f"**Classification:** {severity} ({etiology})")
    else:
      st.success(f"**Classification:** {severity}")

    st.markdown(
        "*Note: This tool is intended to assist clinical judgment and should"
        " always be verified against official institutional guidelines and"
        " complete patient charting.*"
    )