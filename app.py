import streamlit as st
import json
import os
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

st.title("Maternal & Ultrasound Data Collection")

with st.form("data_form"):
    study_id = st.text_input("Patient study ID: (e.g. 001)")
    date_collected = st.date_input("Date of collecting data (DD/MM/Year)")

    st.header("a) Maternal Demographics")
    age = st.number_input("What is the mother’s age in years?", min_value=10, max_value=60, value=None, placeholder="Enter age")
    weight = st.number_input("What is the mother’s weight in kg?", min_value=20.0, value=None, placeholder="Enter weight")
    height = st.number_input("What is the mother’s height in centimeters (cm)?", min_value=50.0, value=None, placeholder="Enter height")

    st.header("b) Maternal Factors")
    num_preg = st.number_input("How many pregnancies that you have had that made at least 6 weeks of gestation age (include miscarriages/abortions/still births and live births)?", min_value=0, value=None, placeholder="Enter number")
    st.subheader("What is the mother’s blood pressure reading?")
    st.markdown("Previous antenatal visit measurement")
    prev_sys = st.number_input("Systolic blood pressure: (previous) (mmHg)", value=None, placeholder="Enter systolic BP")
    prev_dia = st.number_input("Diastolic blood pressure: (previous) (mmHg)", value=None, placeholder="Enter diastolic BP")
    st.markdown("Current antenatal visit")
    curr_sys = st.number_input("Systolic blood pressure: (current) (mmHg)", value=None, placeholder="Enter systolic BP")
    curr_dia = st.number_input("Diastolic blood pressure: (current) (mmHg)", value=None, placeholder="Enter diastolic BP")
    diabetes = st.radio("According to the previous and current antenatal records, does the mother have diabetes?", ["Yes", "No"], index=None)
    bleeding = st.radio("Have you experienced vaginal bleeding since you got this pregnancy?", ["Yes", "No"], index=None)

    st.header("c) Information from Obstetric Ultrasound Report(s) performed prior to 24 weeks of Gestation age")
    scan_date = st.date_input("Which Date (DD/month/year) was the scan performed? If not available indicate NA")
    ga_weeks = st.number_input("What was the Gestation age in weeks determined by the scan?", min_value=0, value=None, placeholder="Enter gestational age")
    fetal_anom = st.radio("Did the scan diagnose any fetal anomalies?", ["Yes", "No"], index=None)
    fetal_desc = st.text_input("If Yes, which anomalies were detected:", key="fetal_desc")
    placenta_anom = st.radio("Did the scan diagnose any placenta anomalies?", ["Yes", "No"], index=None)
    placenta_desc = st.text_input("If Yes, which anomalies were detected:", key="placenta_desc")

    st.header("Current Ultrasound Findings")
    fhr = st.number_input("What is the Fetal Heart Rate (FHR)?", value=None, placeholder="Enter FHR")
    # Fetal structural anomaly (current scan)
    fetal_structural_anom = st.radio("Is there any fetal structural anomaly seen?", ["Yes", "No"], index=None)
    fetal_structural_desc = st.text_input("If Yes Please specify:", key="fetal_structural_desc")

    af = st.selectbox("Basing on the Amniotic fluid Index (AFI) calculated/subjective assessment of amniotic fluid, what can you say about amniotic fluid", [
        "", "Adequate", "Reduced (oligohydromnious)", "Increased (Polyhydramnios)", "Anhydromnious (No pool of amniotic fluid seen)"
    ], index=0)
    placenta_loc = st.selectbox("What is the placenta location?", [
        "", "Fundal", "Fundo-anterior", "Fundo-posterior", "Anterior", "Posterior"
    ], index=0)

    # Placenta abnormality (current scan)
    placenta_abnormal = st.radio("Is there any abnormality of the placenta noted?", ["Yes", "No"], index=None)
    placenta_abnormal_desc = st.text_input("If Yes please specify:", key="placenta_abnormal_desc")

    placenta_grade = st.selectbox("Using the Grannum Placenta Grading system, what is the Placenta Grade?", [
        "", "Grade 0", "Grade I", "Grade II", "Grade III"
    ], index=0)
    efw = st.number_input("What is the estimated Fetal Weight (EFW)?", value=None, placeholder="Enter EFW (g)")
    efw_cat = st.selectbox("Using the Reference WHO fetal growth chart provided in Appendix VIII, categorize the EFW.", [
        "", "Small for Gestation age", "Normal for Gestation age", "Large for Gestation age"
    ], index=0)

    # UAD findings
    uad_findings = st.selectbox("Which of the following best describes the UAD findings?", [
        "", "Positive Diastolic Blood flow is present", "Absent or Reversed Diastolic Blood Flow (ARDBF) is present"
    ], index=0)

    # UAD indices (only if Positive Diastolic Blood flow is present)
    st.markdown("In case in the question above you have selected option A, determine the UAD indices:")
    st.markdown("First Umbilical Artery")
    uad1_sd = st.text_input("S/D (First Umbilical Artery):", key="uad1_sd")
    uad1_mean_sd = st.text_input("Mean S/D (First Umbilical Artery):", key="uad1_mean_sd")
    uad1_pi = st.text_input("PI (First Umbilical Artery):", key="uad1_pi")
    uad1_mean_pi = st.text_input("Mean PI (First Umbilical Artery):", key="uad1_mean_pi")
    uad1_ri = st.text_input("RI (First Umbilical Artery):", key="uad1_ri")
    uad1_mean_ri = st.text_input("Mean RI (First Umbilical Artery):", key="uad1_mean_ri")
    st.markdown("Second Umbilical Artery")
    uad2_sd = st.text_input("S/D (Second Umbilical Artery):", key="uad2_sd")
    uad2_pi = st.text_input("PI (Second Umbilical Artery):", key="uad2_pi")
    uad2_ri = st.text_input("RI (Second Umbilical Artery):", key="uad2_ri")

    # Categorize mean indices
    st.markdown("Using the reference provided in Appendix VI, Categorize the mean Indices accordingly:")
    mean_sd_cat = st.selectbox("Mean S/D", ["", "Normal", "Abnormal"], index=0)
    mean_pi_cat = st.selectbox("Mean PI", ["", "Normal", "Abnormal"], index=0)
    mean_ri_cat = st.selectbox("Mean RI", ["", "Normal", "Abnormal"], index=0)

    submit = st.form_submit_button("Save Data")

if submit:
    record = {
        "study_id": study_id,
        "date_collected": str(date_collected),
        "saved_at": datetime.now().isoformat(),

        "maternal_demographics": {
            "age": age,
            "weight_kg": weight,
            "height_cm": height
        },
        "maternal_factors": {
            "num_pregnancies": num_preg,
            "bp_previous": {"systolic": prev_sys, "diastolic": prev_dia},
            "bp_current": {"systolic": curr_sys, "diastolic": curr_dia},
            "diabetes": diabetes == "Yes",
            "vaginal_bleeding": bleeding == "Yes"
        },
        "prior_ultrasound": {
            "scan_date": str(scan_date),
            "gestational_age_weeks": ga_weeks,
            "fetal_anomalies": {
                "present": fetal_anom == "Yes",
                "description": fetal_desc
            },
            "placenta_anomalies": {
                "present": placenta_anom == "Yes",
                "description": placenta_desc
            }
        },
        "current_ultrasound": {
            "fhr": fhr,
            "amniotic_fluid": af,
            "placenta_location": placenta_loc,
            "placenta_grade": placenta_grade,
            "efw_g": efw,
            "efw_category": efw_cat
        }
    }

    filename = f"{study_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(record, f, indent=4)

    st.success(f"Data saved to {filepath}")