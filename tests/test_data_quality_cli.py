from audit_rag.quality.data_quality import validate_normalized_data


def test_validate_normalized_data_passes_current_repository() -> None:
    result = validate_normalized_data()

    assert result["status"] == "ok"
    assert result["checked_files"] >= 100
    assert result["violations"] == []
