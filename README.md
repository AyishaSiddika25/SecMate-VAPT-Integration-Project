# SecMate – Agentic VAPT Integration Project

### AI-Assisted Security Assessment Prototype

SecMate is a Streamlit-based security assessment prototype that integrates Red Team attack generation, Blue Team response evaluation, and Vulnerability Assessment and Penetration Testing (VAPT) analysis into a single workflow.

The project is designed to demonstrate how security testing components can work together to assess AI-targeted applications, organize findings, and generate assessment reports.

> **Project Status:** Development Prototype
> **Assessment Mode:** Simulated
> **VAPT Mode:** Rule-Based

---

## 📌 Project Overview

SecMate combines multiple security assessment components into one application.

The prototype generates predefined adversarial prompts, evaluates simulated target responses, analyzes security evidence, and presents assessment results through a Streamlit interface.

The project focuses on modular integration, assessment workflow management, and report generation.

---

## 🎯 Objectives

* Integrate Red Team and Blue Team assessment components.
* Generate predefined adversarial prompts for AI security testing.
* Evaluate target responses using rule-based evaluation logic.
* Perform rule-based VAPT evidence analysis.
* Present assessment results through a centralized dashboard.
* Store assessment history and generate downloadable JSON reports.
* Establish a foundation for future live AI security testing.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │   Streamlit UI       │
                 │   SecMate Dashboard  │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   Assessment Engine  │
                 │    core/engine.py    │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
    ┌─────────▼─────────┐      ┌──────────▼────────┐
    │     Red Team      │      │     Blue Team     │
    │ Attack Generation │─────▶│ Response Evaluation│
    └───────────────────┘      └───────────────────┘
                                          │
                                ┌─────────▼─────────┐
                                │   VAPT Analyzer   │
                                │  Rule-Based Logic │
                                └─────────┬─────────┘
                                          │
                                ┌─────────▼─────────┐
                                │ Reports & Storage │
                                │ SQLite / JSON     │
                                └───────────────────┘
```

---

## ⚙️ Key Features

### 1. Red Team – Attack Generation

The Red Team module generates predefined adversarial prompts for AI security assessment.

Supported attack categories include:

* Prompt Injection
* Sensitive Information Disclosure
* Role Override
* Jailbreak Attempts

The module supports configurable assessment intensity levels.

**File:** `red_team/attack_generator.py`

### 2. Blue Team – Response Evaluation

The Blue Team module evaluates target responses using rule-based indicators.

It identifies potential refusal or disclosure patterns and assigns evaluation verdicts, severity, and explanations.

**File:** `blue_team/blue_team_judge.py`

### 3. Assessment Engine

The assessment engine integrates Red Team attack generation with Blue Team response evaluation.

It manages the assessment workflow and produces structured assessment results, including test counts, verdicts, and evaluation details.

The current prototype uses simulated target responses.

**File:** `core/engine.py`

### 4. VAPT Security Analysis

The VAPT module performs rule-based security evidence analysis and organizes potential findings for review.

It is designed to support the assessment workflow and provide structured security findings.

**Directory:** `vapt/`

### 5. Streamlit Dashboard

The Streamlit application provides a centralized interface for interacting with the prototype.

Implemented interface areas include:

* Dashboard
* New Assessment
* Assessment Summary
* Individual Test Results
* VAPT Findings
* Reports

**File:** `app/streamlit_app.py`

### 6. Assessment Reports

The application is designed to store assessment history using SQLite and provide downloadable JSON reports.

Report availability and persistence should be verified through the running application.

**Directory:** `reports/`

---

## 📂 Project Structure

```text
SecMate-VAPT-Integration-Project/
│
├── app/
│   └── streamlit_app.py
│
├── core/
│   ├── engine.py
│   ├── models.py
│   ├── database.py
│   └── config_loader.py
│
├── red_team/
│   └── attack_generator.py
│
├── blue_team/
│   └── blue_team_judge.py
│
├── vapt/
│   ├── security_analyzer.py
│   ├── security_decision.py
│   └── validate_llm_output.py
│
├── config/
│   └── settings.yaml
│
├── reports/
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

| Technology   | Purpose                       |
| ------------ | ----------------------------- |
| Python       | Core application development  |
| Streamlit    | Interactive web interface     |
| PyYAML       | Configuration loading         |
| SQLite       | Assessment history storage    |
| JSON         | Structured assessment reports |
| Git & GitHub | Version control               |

---

## 🚀 Installation and Setup

### Prerequisites

* Python 3.10 or later
* Git
* Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/AyishaSiddika25/SecMate-VAPT-Integration-Project.git
```

### Step 2: Navigate to the Project

```bash
cd SecMate-VAPT-Integration-Project
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python -m streamlit run app/streamlit_app.py
```

The application will open in your default browser. If it does not, open the local URL displayed in the terminal.

---

## 🧪 Assessment Workflow

1. Launch the SecMate application.
2. Navigate to **New Assessment**.
3. Select the assessment intensity.
4. Run the assessment.
5. Review generated Red Team prompts.
6. Examine Blue Team evaluation results.
7. Review available VAPT findings.
8. Check assessment history in Reports.
9. Download the assessment report in JSON format, if available.

---

## ⚠️ Current Limitations

SecMate is currently a development prototype and should not be considered a production-ready security testing platform.

* Target responses are simulated rather than generated by a live AI model.
* Red Team attacks are based on predefined attack patterns.
* Blue Team evaluation uses rule-based logic.
* VAPT analysis is rule-based and does not constitute a comprehensive vulnerability scan.
* The prototype does not establish that a real target is secure or vulnerable.
* Results require validation before being treated as confirmed security findings.

A successful simulated assessment does not prove that an AI system is secure against real-world attacks.

---

## 🔮 Future Enhancements

* Integrate live AI model endpoints through configurable API settings.
* Expand adversarial attack generation and test coverage.
* Improve response evaluation with contextual analysis.
* Integrate additional static and dynamic security testing tools.
* Implement evidence-based finding validation.
* Enhance severity classification and risk prioritization.
* Improve assessment reporting and visualization.
* Add automated testing and CI/CD integration.

---

## 👩‍💻 Project Information

**Project:** SecMate – Agentic VAPT Integration Project
**GitHub:** [AyishaSiddika25](https://github.com/AyishaSiddika25)
**Repository:** [SecMate-VAPT-Integration-Project](https://github.com/AyishaSiddika25/SecMate-VAPT-Integration-Project)

---

## 📄 Disclaimer

This project is developed for educational, research, and prototype demonstration purposes.

The current implementation uses simulated target responses and rule-based evaluation. It is not a substitute for professional penetration testing or a comprehensive security audit.

Only perform security testing against systems for which you have explicit authorization.

