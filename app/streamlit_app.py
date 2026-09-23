import json
import html
import streamlit as st

from core.engine import run_assessment
from core.database import (
    initialize_database,
    save_assessment,
    get_all_assessments
)
from vapt.security_analyzer import analyze_security_evidence


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SecMate",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #070f20;
    color: #e5eefc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #09172e;
    border-right: 1px solid #18345b;
}

/* Headings */

h1, h2, h3 {
    color: #edf4ff !important;
}

/* Metric cards */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #10264a, #0c1c37);
    border: 1px solid #1e477c;
    padding: 18px;
    border-radius: 12px;
    min-height: 115px;
}

[data-testid="stMetricLabel"] {
    color: #a9c7ed !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* Buttons */

div.stButton > button {
    background: linear-gradient(90deg, #1266e8, #087fce);
    color: white;
    border: 1px solid #3287ff;
    border-radius: 9px;
    font-weight: 600;
}

div.stButton > button:hover {
    background: #1d75f0;
    color: white;
}

/* Download buttons */

div.stDownloadButton > button {
    background: #102c50;
    color: #dcecff;
    border: 1px solid #28578d;
    border-radius: 8px;
}

/* Expanders */

[data-testid="stExpander"] {
    background: #0d1d37;
    border: 1px solid #203d66;
    border-radius: 10px;
}

/* Dashboard context cards */

.sec-card {
    background: linear-gradient(145deg, #0e2242, #0a1932);
    border: 1px solid #1c477b;
    border-radius: 14px;
    padding: 22px;
    min-height: 185px;
    margin-bottom: 12px;
}

.sec-card-label {
    color: #8eb5e9;
    font-size: 13px;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.sec-card-title {
    color: #f1f6ff;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 9px;
}

.sec-card-desc {
    color: #bfd2ed;
    font-size: 15px;
    line-height: 1.6;
}

/* Module cards */

.module-card {
    background: linear-gradient(145deg, #10264a, #0b1a34);
    border: 1px solid #244a7d;
    border-radius: 14px;
    padding: 22px;
    min-height: 205px;
    margin-bottom: 12px;
}

.module-icon {
    font-size: 27px;
    margin-bottom: 10px;
}

.module-title {
    color: #f1f6ff;
    font-size: 21px;
    font-weight: 700;
}

.module-subtitle {
    color: #8fbdf6;
    font-size: 14px;
    margin-bottom: 12px;
}

.module-description {
    color: #c1d2e9;
    font-size: 14px;
    line-height: 1.6;
}

/* Information panels */

.info-card {
    background: #0d2040;
    border: 1px solid #214777;
    border-radius: 14px;
    padding: 22px;
    min-height: 230px;
    margin-bottom: 12px;
}

.info-title {
    color: #f1f6ff;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 14px;
}

.info-text {
    color: #bfd2ed;
    font-size: 14px;
    line-height: 1.8;
}

/* Prototype badge */

.prototype-badge {
    display: inline-block;
    background: #063e3a;
    color: #5eead4;
    border: 1px solid #0f766e;
    border-radius: 20px;
    padding: 6px 13px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(value, default="N/A"):
    """Return safe text for HTML display."""

    if value is None:
        return default

    return html.escape(str(value))


def safe_json(data):
    """Convert Python data into formatted JSON."""

    return json.dumps(data, indent=4, default=str)


def safe_get_history():
    """Retrieve assessment history safely."""

    try:
        history = get_all_assessments()

        if isinstance(history, list):
            return history

        return []

    except Exception:
        return []


def render_context_card(label, title, description, icon):
    """Render a dashboard overview card."""

    st.markdown(
        f"""
        <div class="sec-card">
            <div class="sec-card-label">{label}</div>
            <div class="sec-card-title">
                {safe_text(icon)} {safe_text(title)}
            </div>
            <div class="sec-card-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_finding(finding):
    """Display details of a VAPT finding."""

    st.write("**Status:**", finding.get("status", "N/A"))
    st.write("**Category:**", finding.get("category", "N/A"))
    st.write("**Description:**", finding.get("description", "N/A"))
    st.write("**Evidence:**", finding.get("evidence", "N/A"))
    st.write(
        "**Recommendation:**",
        finding.get("recommendation", "N/A")
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 🛡️ SecMate")
st.sidebar.caption("AGENTIC VAPT INTEGRATION")

st.sidebar.divider()

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

st.sidebar.caption("🛡️ SecMate")
st.sidebar.caption("Smarter Testing. Safer Systems.")
st.sidebar.caption("Development Prototype")


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # HEADER — SecMate only
    # --------------------------------------------------------

    header_col1, header_col2 = st.columns([5, 1])

    with header_col1:
        st.title("🛡️ SecMate")

        st.caption(
            "AI-Assisted Security Assessment Platform  |  "
            "Red Team + Blue Team + VAPT"
        )

    with header_col2:
        st.markdown(
            '<div class="prototype-badge">● Prototype Mode</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------------
    # LOAD ASSESSMENT HISTORY
    # --------------------------------------------------------

    history = safe_get_history()

    st.session_state.assessment_history = history

    total_assessments = len(history)

    completed_count = sum(
        1 for item in history
        if item.get("verdict")
    )

    total_findings = sum(
        len(item.get("vapt_findings", []))
        for item in history
        if isinstance(item.get("vapt_findings", []), list)
    )

    # Latest assessment for context cards
    latest = history[0] if history else {}

    # --------------------------------------------------------
    # CONTEXT CARDS
    # --------------------------------------------------------

    st.subheader("Assessment Overview")

    latest_target = latest.get("target", "DBGuard-Bot")

    latest_intensity = latest.get("intensity", "Basic")

    # Map engine intensity values to dashboard labels
    intensity_map = {
        "low": "Basic",
        "medium": "Standard",
        "high": "Advanced",
        "basic": "Basic",
        "standard": "Standard",
        "advanced": "Advanced"
    }

    display_intensity = intensity_map.get(
        str(latest_intensity).lower(),
        str(latest_intensity)
    )

    depth_descriptions = {
        "Basic": "Basic assessment intensity",
        "Standard": "Standard assessment intensity",
        "Advanced": "Advanced assessment intensity"
    }

    depth_description = depth_descriptions.get(
        display_intensity,
        "Run an assessment to view its intensity."
    )

    card1, card2, card3 = st.columns(3)

    with card1:
        render_context_card(
            "TARGET PERSONA",
            latest_target,
            "AI agent selected for security assessment, "
            "response evaluation, and security analysis.",
            "🤖"
        )

    with card2:
        render_context_card(
            "ATTACK SCENARIO",
            "Adversarial Prompt Testing",
            "Evaluates prompt injection, role override, "
            "jailbreak attempts, and sensitive information "
            "disclosure using simulated tests.",
            "🎯"
        )

    with card3:
        render_context_card(
            "ASSESSMENT DEPTH",
            display_intensity,
            depth_description,
            "📊"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # METRIC CARDS
    # --------------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Assessments",
        total_assessments
    )

    metric2.metric(
        "Completed",
        completed_count
    )

    metric3.metric(
        "In Progress",
        0
    )

    metric4.metric(
        "VAPT Indicators",
        total_findings
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # RECENT ASSESSMENTS
    # --------------------------------------------------------

    st.subheader("🕒 Recent Assessments")

    if history:

        recent_rows = []

        for item in history[:5]:

            recent_rows.append({
                "ID": item.get("assessment_id", "N/A"),
                "Target": item.get("target", "N/A"),
                "Intensity": item.get("intensity", "N/A"),
                "Status": item.get("verdict", "N/A"),
                "Date": item.get("timestamp", "N/A")
            })

        st.dataframe(
            recent_rows,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No assessments found. Run your first assessment "
            "to see results here."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SECURITY MODULE CARDS
    # --------------------------------------------------------

    st.subheader("Security Assessment Modules")

    module1, module2, module3 = st.columns(3)

    with module1:

        st.markdown("""
        <div class="module-card">
            <div class="module-icon">🔴</div>
            <div class="module-title">Red Team</div>
            <div class="module-subtitle">Attack Generation</div>
            <div class="module-description">
                Generate adversarial prompts to test AI
                behavior and identify potential weaknesses.
                <br><br>
                Prompt Injection • Role Override • Jailbreak
            </div>
        </div>
        """, unsafe_allow_html=True)

    with module2:

        st.markdown("""
        <div class="module-card">
            <div class="module-icon">🔵</div>
            <div class="module-title">Blue Team</div>
            <div class="module-subtitle">Response Evaluation</div>
            <div class="module-description">
                Evaluate simulated target responses using
                rule-based logic and identify cases requiring
                further review.
                <br><br>
                Defended • Needs Review • Exposed
            </div>
        </div>
        """, unsafe_allow_html=True)

    with module3:

        st.markdown("""
        <div class="module-card">
            <div class="module-icon">🛡️</div>
            <div class="module-title">VAPT Analysis</div>
            <div class="module-subtitle">Security Findings</div>
            <div class="module-description">
                Analyze available security evidence and
                organize potential indicators for review.
                <br><br>
                Findings • Risk Indicators • Recommendations
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # INFORMATION PANELS
    # --------------------------------------------------------

    info1, info2 = st.columns(2)

    with info1:

        st.markdown("""
        <div class="info-card">
            <div class="info-title">💡 Why it matters</div>

            <div class="info-text">
                SecMate brings together attack generation,
                response evaluation, and VAPT analysis in
                one assessment workflow.
                <br><br>

                It helps organize simulated security test
                results and potential indicators so they
                can be reviewed in a structured way.
                <br><br>

                The current prototype demonstrates workflow
                integration and does not establish real-world
                AI system security.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with info2:

        st.markdown("""
        <div class="info-card">
            <div class="info-title">📘 How to use</div>

            <div class="info-text">
                <b>1.</b> Go to New Assessment and enter a target name.
                <br>

                <b>2.</b> Select the assessment type and intensity.
                <br>

                <b>3.</b> Run the assessment to generate simulated
                Red Team tests and Blue Team results.
                <br>

                <b>4.</b> Review VAPT indicators and recommendations.
                <br>

                <b>5.</b> Open Reports to download assessment JSON.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "💡 Tip: Start with Basic assessment intensity "
        "to explore the workflow."
    )


# ============================================================
# NEW ASSESSMENT
# ============================================================

elif page == "New Assessment":

    st.title("🧪 New Security Assessment")

    st.caption(
        "Configure and run a simulated AI security assessment."
    )

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

            try:

                # Run simulated assessment
                result = run_assessment(
                    target_name.strip(),
                    intensity
                )

                result["assessment_type"] = assessment_type

                # Run rule-based VAPT analysis
                vapt_result = analyze_security_evidence(result)

                result["vapt_analysis"] = vapt_result

                result["vapt_findings"] = vapt_result.get(
                    "findings", []
                )

                # Save to SQLite
                save_assessment(result)

                # Refresh history
                st.session_state.assessment_history = safe_get_history()

                st.success("Assessment completed and saved!")

                st.subheader("Assessment Results")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Target",
                    result.get("target", "N/A")
                )

                col2.metric(
                    "Verdict",
                    result.get("verdict", "N/A")
                )

                col3.metric(
                    "Severity",
                    result.get("severity", "N/A")
                )

                st.write(
                    "**Assessment ID:**",
                    result.get("assessment_id", "N/A")
                )

                st.write(
                    "**Timestamp:**",
                    result.get("timestamp", "N/A")
                )

                st.write(
                    "**Assessment Type:**",
                    assessment_type
                )

                # Red Team
                with st.expander(
                    "🔴 Red Team Attack",
                    expanded=True
                ):
                    st.code(
                        result.get("attack_prompt", "N/A")
                    )

                # Target response
                with st.expander(
                    "🤖 Target AI Response",
                    expanded=True
                ):
                    st.write(
                        result.get("target_response", "N/A")
                    )

                # Blue Team
                with st.expander(
                    "🔵 Blue Team Evaluation",
                    expanded=True
                ):
                    st.write(
                        result.get("explanation", "N/A")
                    )

                # VAPT Analysis
                st.divider()

                st.subheader("🛡️ VAPT Analysis")

                st.write(
                    "Indicators detected:",
                    vapt_result.get("finding_count", 0)
                )

                st.caption(
                    "Analysis Mode: "
                    + str(vapt_result.get("analysis_mode", "N/A"))
                )

                for finding in result["vapt_findings"]:

                    with st.expander(
                        f"{finding.get('finding_id', 'N/A')} | "
                        f"{finding.get('title', 'Finding')} | "
                        f"{finding.get('severity', 'N/A')}"
                    ):

                        show_finding(finding)

                # Download report
                report_json = safe_json(result)

                st.download_button(
                    label="⬇️ Download Assessment Report (JSON)",
                    data=report_json,
                    file_name=(
                        f"{result.get('assessment_id', 'assessment')}.json"
                    ),
                    mime="application/json"
                )

                st.caption(
                    "Simulated assessment — not a live security test."
                )

            except Exception as error:

                st.error("Assessment failed.")
                st.exception(error)


# ============================================================
# VAPT FINDINGS
# ============================================================

elif page == "VAPT Findings":

    st.title("🛡️ VAPT Findings")

    history = safe_get_history()

    st.session_state.assessment_history = history

    all_findings = []

    for assessment in history:

        findings = assessment.get("vapt_findings", [])

        if not isinstance(findings, list):
            continue

        for finding in findings:

            if not isinstance(finding, dict):
                continue

            finding_copy = finding.copy()

            finding_copy["assessment_id"] = assessment.get(
                "assessment_id", "N/A"
            )

            finding_copy["target"] = assessment.get(
                "target", "N/A"
            )

            all_findings.append(finding_copy)

    if all_findings:

        st.write(f"Total indicators: {len(all_findings)}")

        for finding in reversed(all_findings):

            with st.expander(
                f"{finding.get('finding_id', 'N/A')} | "
                f"{finding.get('title', 'Finding')} | "
                f"{finding.get('severity', 'N/A')}"
            ):

                st.write(
                    "**Target:**",
                    finding.get("target", "N/A")
                )

                st.write(
                    "**Assessment ID:**",
                    finding.get("assessment_id", "N/A")
                )

                show_finding(finding)

    else:

        st.info(
            "No VAPT indicators available. "
            "Run a new assessment first."
        )

    st.caption(
        "These are rule-based indicators, not confirmed vulnerabilities."
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("📄 Assessment Reports")

    history = safe_get_history()

    st.session_state.assessment_history = history

    if history:

        st.success(
            f"{len(history)} assessment(s) available."
        )

        for item in history:

            st.divider()

            st.write(
                "**Assessment ID:**",
                item.get("assessment_id", "N/A")
            )

            st.write(
                "**Target:**",
                item.get("target", "N/A")
            )

            st.write(
                "**Verdict:**",
                item.get("verdict", "N/A")
            )

            st.write(
                "**Timestamp:**",
                item.get("timestamp", "N/A")
            )

            report_json = safe_json(item)



            st.download_button(
                label=(
                    "⬇️ Download "
                    + str(item.get("assessment_id", "Assessment"))
                ),
                data=report_json,
                file_name=(
                    f"{item.get('assessment_id', 'assessment')}.json"
                ),
                mime="application/json",
                key=f"download_{item.get('assessment_id', 'unknown')}"
            )

        # Download all reports
        all_reports = safe_json(history)

        st.download_button(
            label="⬇️ Download All Assessment Reports",
            data=all_reports,
            file_name="SecMate_All_Assessments.json",
            mime="application/json"
        )

    else:

        st.info("No assessment reports available yet.")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SecMate | Agentic AI Security Assessment Platform | "
    "Development Prototype"
)
