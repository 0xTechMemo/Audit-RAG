STAGE_REGISTRY = {
    "candidate-triage": {
        "required_queries": [
            "case_report",
            "vulnerability_pattern",
            "false_positive_case",
            "validation_recipe",
        ],
        "required_output_fields": [
            "likely_root_cause",
            "false_positive_risks",
            "submission_blockers",
            "sources",
        ],
    }
}
