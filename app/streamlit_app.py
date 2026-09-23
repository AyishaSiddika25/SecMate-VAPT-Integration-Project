import json
import streamlit as st

from core.engine import run_assessment
from core.database import (
    initialize_database,
    save_assessment,
    get_all_assessments
)
from vapt.security_analyzer import analyze_security_evidence


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SecMate",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- DATABASE INITIALIZATION ----------------

initialize_database()

if "assessment_history" not in st.session_state:
    st.session_state.assessment_history = get_all_assessments()


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e2e8f0;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetric"] {
    background-color: #111827;
    padding: 18px;
    border: 1px solid #263449;
    border-radius: 12px;
}

div.stButton > button {
    background-color: #0d9488;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# 🛡️ SecMate")
st.sidebar.caption("AI SECURITY PLATFORM")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "New Assessment",
        "VAPT Findings",
        "Reports"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Agentic VAPT Integration")
st.sidebar.caption("Development Prototype")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("🛡️ SecMate")
    st.caption("AI SECURITY & VULNERABILITY ASSESSMENT")

    st.divider()

    history = get_all_assessments()
    st.session_state.assessment_history = history

    total_assessments = len(history)

    defended_count = sum(
        1 for item in history
        if item.get("verdict") == "DEFENDED"
    )

    total_indicators = sum(
        len(item.get("vapt_findings", []))
        for item in history
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Assessments Run", total_assessments)
    col2.metric("Defended Assessments", defended_count)
    col3.metric("VAPT Indicators", total_indicators)

    st.subheader("Assessment Workflow")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown("🔴 **RED TEAM**")
    c1.caption("Attack Simulation")

    c2.markdown("🤖 **TARGET AI**")
    c2.caption("Response Analysis")

    c3.markdown("🔵 **BLUE TEAM**")
    c3.caption("Defense Evaluation")

    c4.markdown("🛡️ **AGENTIC VAPT**")
    c4.caption("Rule-Based Analysis")

    st.divider()

    st.subheader("Recent Assessments")

    if history:

        for item in history[:5]:

            st.write(
                f"**{item['assessment_id']}** | "
                f"{item['target']} | "
                f"{item['verdict']} | "
                f"{item['timestamp']}"
            )

    else:
        st.info("No assessments have been run yet.")


# ---------------- NEW ASSESSMENT ----------------

elif page == "New Assessment":

    st.title("New Security Assessment")

    target_name = st.text_input(
        "Target AI Agent",
        value="DBGuard-Bot"
    )

    assessment_type = st.selectbox(
        "Assessment Type",
        [
            "Red Team–Blue Team Assessment",
            "VAPT Security Analysis",
            "Combined Security Assessment"
        ]
    )

    intensity = st.select_slider(
        "Assessment Intensity",
        options=["Basic", "Standard", "Advanced"],
        value="Basic"
    )

    st.warning(
        "This prototype uses simulated target responses and "
        "rule-based evidence analysis. It does not perform "
        "live AI testing or network vulnerability scanning."
    )

    if st.button("▶ Run Assessment", type="primary"):

        if not target_name.strip():

            st.error("Enter a target AI agent name.")

        else:

            # Run simulated assessment
            result = run_assessment(
                target_name.strip(),
                intensity
            )

            result["assessment_type"] = assessment_type

            # Run rule-based VAPT analysis
            vapt_result = analyze_security_evidence(result)

            result["vapt_analysis"] = vapt_result
            result["vapt_findings"] = vapt_result["findings"]

            # Save assessment to SQLite
            save_assessment(result)

            # Refresh assessment history
            st.session_state.assessment_history = get_all_assessments()

            st.success("Assessment completed and saved!")

            st.subheader("Assessment Results")

            col1, col2, col3 = st.columns(3)

            col1.metric("Target", result["target"])
            col2.metric("Verdict", result["verdict"])
            col3.metric("Severity", result["severity"])

            st.write("**Assessment ID:**", result["assessment_id"])
            st.write("**Timestamp:**", result["timestamp"])
            st.write("**Assessment Type:**", assessment_type)

            with st.expander("🔴 Red Team Attack", expanded=True):
                st.code(result["attack_prompt"])

            with st.expander("🤖 Target AI Response", expanded=True):
                st.write(result["target_response"])

            with st.expander("🔵 Blue Team Evaluation", expanded=True):
                st.write(result["explanation"])

            # VAPT Analysis
            st.divider()
            st.subheader("🛡️ VAPT Analysis")

            st.write(
                f"Indicators detected: {vapt_result['finding_count']}"
            )

            st.caption(
                f"Analysis Mode: {vapt_result['analysis_mode']}"
            )

            for finding in vapt_result["findings"]:

                with st.expander(
                    f"{finding['finding_id']} | "
                    f"{finding['title']} | "
                    f"{finding['severity']}"
                ):

                    st.write("**Status:**", finding["status"])
                    st.write("**Category:**", finding["category"])
                    st.write("**Description:**", finding["description"])
                    st.write("**Evidence:**", finding["evidence"])
                    st.write("**Recommendation:**", finding["recommendation"])

            # Download assessment report
            report_json = json.dumps(result, indent=4)

            st.download_button(
                label="⬇️ Download Assessment Report (JSON)",
                data=report_json,
                file_name=f"{result['assessment_id']}.json",
                mime="application/json"
            )

            st.caption(
                "Simulated assessment — not a live security test."
            )


# ---------------- VAPT FINDINGS ----------------

elif page == "VAPT Findings":

    st.title("🛡️ VAPT Findings")

    history = get_all_assessments()
    st.session_state.assessment_history = history

    all_findings = []

    for assessment in history:

        for finding in assessment.get("vapt_findings", []):

            finding_copy = finding.copy()

            finding_copy["assessment_id"] = assessment["assessment_id"]
            finding_copy["target"] = assessment["target"]

            all_findings.append(finding_copy)

    if all_findings:

        st.write(f"Total indicators: {len(all_findings)}")

        for finding in reversed(all_findings):

            with st.expander(
                f"{finding['finding_id']} | "
                f"{finding['title']} | "
                f"{finding['severity']}"
            ):

                st.write("**Target:**", finding["target"])
                st.write("**Assessment ID:**", finding["assessment_id"])
                st.write("**Status:**", finding["status"])
                st.write("**Category:**", finding["category"])
                st.write("**Description:**", finding["description"])
                st.write("**Evidence:**", finding["evidence"])
                st.write("**Recommendation:**", finding["recommendation"])

    else:

        st.info(
            "No VAPT indicators available. Run a new assessment first."
        )

    st.caption(
        "These are rule-based indicators, not confirmed vulnerabilities."
    )


# ---------------- REPORTS ----------------

elif page == "Reports":

    st.title("📄 Assessment Reports")

    history = get_all_assessments()
    st.session_state.assessment_history = history

    if history:

        st.success(f"{len(history)} assessment(s) available.")

        for item in history:

            st.divider()

            st.write(f"**Assessment ID:** {item['assessment_id']}")
            st.write(f"**Target:** {item['target']}")
            st.write(f"**Verdict:** {item['verdict']}")
            st.write(f"**Timestamp:** {item['timestamp']}")

            report_json = json.dumps(item, indent=4)

            st.download_button(
                label=f"⬇️ Download {item['assessment_id']}",
                data=report_json,
                file_name=f"{item['assessment_id']}.json",
                mime="application/json",
                key=f"download_{item['assessment_id']}"
            )

        # Download all reports
        all_reports = json.dumps(history, indent=4)

        st.download_button(
            label="⬇️ Download All Assessment Reports",
            data=all_reports,
            file_name="SecMate_All_Assessments.json",
            mime="application/json"
        )

    else:

        st.info("No assessment reports available yet.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "SecMate | Agentic AI Security Assessment Platform"
)