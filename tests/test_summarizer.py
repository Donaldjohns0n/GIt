"""Unit tests for the research summary generator."""

from src import ResearchSummaryGenerator


def word_count(text: str) -> int:
    return len([word for word in text.split() if word])


def test_missing_data_response_generates_fixed_summary():
    generator = ResearchSummaryGenerator()
    result = generator.generate_summary(["…", "…"])

    assert result.title == "Insufficient Data to Summarize Research"
    assert len(result.citations) == 9
    assert all(citation == [1, 2] for citation in result.citations)
    assert word_count(result.summary) >= 350


def test_substantive_summary_meets_word_target():
    bullet_points = [
        (
            "The study enrolled 200 participants drawn from three community "
            "clinics."
        ),
        (
            "Researchers documented a 1.2 percent improvement in HbA1c "
            "following the six-month intervention."
        ),
        (
            "Adherence rates exceeded 90 percent throughout the observation "
            "period."
        ),
    ]
    generator = ResearchSummaryGenerator(word_target=200)
    result = generator.generate_summary(bullet_points)

    assert result.title == "Research Summary"
    assert word_count(result.summary) >= 200
    expected_min_sentences = len(bullet_points) * 2 + 4
    assert len(result.citations) >= expected_min_sentences


def test_padding_uses_all_indices_for_citations():
    bullet_points = [
        (
            "Observation protocols were pre-registered before data "
            "collection began."
        ),
    ]
    generator = ResearchSummaryGenerator(word_target=120)
    result = generator.generate_summary(bullet_points)

    all_indices = {1}
    for citation in result.citations:
        assert set(citation) == all_indices
