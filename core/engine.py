"""
SecMate Assessment Engine

Connects the Red Team attack generator and Blue Team evaluator.

IMPORTANT:
This version uses simulated target responses.
It does not perform live AI testing.
"""

from datetime import datetime
from uuid import uuid4

from core.config_loader import load_config, get_target_config

from red_team.attack_generator import generate_attacks
from blue_team.blue_team_judge import evaluate_response


# Map Streamlit intensity labels to generator intensity levels
INTENSITY_MAP = {
    "basic": "low",
    "standard": "medium",
    "advanced": "high",
}


def simulate_target_response(attack):
    """
    Return a simulated target response.

    This function does NOT call a real AI model.
    """

    return (
        "I cannot comply with this request. "
        "I must follow my instructions and protect "
        "confidential information."
    )


def run_assessment(target_name=None, intensity=None):
    """
    Run a simulated Red Team–Blue Team assessment.

    Generates multiple attacks, simulates target responses,
    and evaluates each response using the Blue Team.

    Returns a dictionary compatible with the existing
    SecMate Streamlit app.
    """

    # ---------------------------------
    # 1. Load configuration
    # ---------------------------------

    config = load_config()
    target_config = get_target_config()

    if not target_name:
        target_name = target_config.get(
            "name", "Default AI Target"
        )

    if not intensity:
        intensity = config.get(
            "assessment", {}
        ).get("default_intensity", "low")

    # Normalize intensity
    intensity_input = str(intensity).strip().lower()

    intensity_level = INTENSITY_MAP.get(
        intensity_input,
        intensity_input
    )

    if intensity_level not in ["low", "medium", "high"]:
        raise ValueError(
            "Invalid intensity. Use Basic, Standard, "
            "Advanced, low, medium, or high."
        )

    # ---------------------------------
    # 2. Generate assessment metadata
    # ---------------------------------

    assessment_id = f"SM-{uuid4().hex[:8].upper()}"

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    # ---------------------------------
    # 3. Red Team: Generate attacks
    # ---------------------------------

    attacks = generate_attacks(
        intensity=intensity_level
    )

    # ---------------------------------
    # 4. Simulated target + Blue Team
    # ---------------------------------

    test_results = []

    for attack in attacks:

        # Simulate target response
        target_response = simulate_target_response(attack)

        # Evaluate response using Blue Team
        evaluation = evaluate_response(
            attack,
            target_response
        )

        # Store complete test result
        test_result = {
            **attack,
            "target_response": target_response,
            "verdict": evaluation["verdict"],
            "severity": evaluation["severity"],
            "explanation": evaluation["explanation"],
            "evaluation_mode": evaluation["evaluation_mode"],
        }

        test_results.append(test_result)

    # ---------------------------------
    # 5. Calculate overall verdict
    # ---------------------------------

    total_tests = len(test_results)

    defended_tests = sum(
        1 for test in test_results
        if test["verdict"] == "DEFENDED"
    )

    review_tests = total_tests - defended_tests

    if total_tests > 0 and defended_tests == total_tests:

        overall_verdict = "DEFENDED"
        overall_severity = "NONE"

        overall_explanation = (
            f"All {total_tests} simulated test responses "
            "contained refusal indicators. This is a "
            "preliminary rule-based result, not proof "
            "of security against real attacks."
        )

    else:

        overall_verdict = "NEEDS_REVIEW"
        overall_severity = "PENDING"

        overall_explanation = (
            f"{review_tests} of {total_tests} simulated "
            "test responses require further review."
        )

    # ---------------------------------
    # 6. Backward-compatible fields
    # ---------------------------------

    # Preserve fields expected by the current Streamlit UI
    if test_results:
        first_test = test_results[0]

        attack_prompt = first_test["prompt"]
        first_target_response = first_test["target_response"]

    else:
        attack_prompt = ""
        first_target_response = ""

    # ---------------------------------
    # 7. Return assessment result
    # ---------------------------------

    return {
        "assessment_id": assessment_id,
        "timestamp": timestamp,
        "target": target_name,
        "intensity": intensity,
        "attack_prompt": attack_prompt,
        "target_response": first_target_response,
        "verdict": overall_verdict,
        "severity": overall_severity,
        "explanation": overall_explanation,
        "assessment_mode": "SIMULATED",
        "total_tests": total_tests,
        "defended_tests": defended_tests,
        "needs_review_tests": review_tests,
        "test_results": test_results,
    }


# ---------------------------------
# Standalone test
# ---------------------------------

if __name__ == "__main__":

    result = run_assessment(
        target_name="SecMate Demo Target",
        intensity="Basic"
    )

    print("\nSecMate Integrated Assessment")
    print("=" * 40)

    print("Assessment ID:", result["assessment_id"])
    print("Target:", result["target"])
    print("Intensity:", result["intensity"])
    print("Assessment Mode:", result["assessment_mode"])

    print("\nTotal Tests:", result["total_tests"])
    print("Defended:", result["defended_tests"])
    print("Needs Review:", result["needs_review_tests"])

    print("\nOverall Verdict:", result["verdict"])
    print("Severity:", result["severity"])
    print("Explanation:", result["explanation"])

    print("\nIndividual Test Results")
    print("-" * 40)

    for test in result["test_results"]:

        print(f"\n{test['attack_id']} | {test['category']}")
        print("Prompt:", test["prompt"])
        print("Response:", test["target_response"])
        print("Verdict:", test["verdict"])
        print("Severity:", test["severity"])