def run_basic_eval(output: dict):
    """
    Basic structural evaluation for generated test cases.
    This does NOT judge correctness, only format and completeness.
    """

    assert "status" in output, "Missing status field"
    assert "use_cases" in output, "Missing use_cases field"
    assert isinstance(output["use_cases"], list), "use_cases must be a list"

    for uc in output["use_cases"]:
        assert uc.get("use_case_title"), "Missing use_case_title"
        assert uc.get("steps"), "Missing steps"
        assert uc.get("expected_results"), "Missing expected_results"
