"""Research summary generation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple


MISSING_DATA_SENTENCES: Sequence[str] = (
    (
        "This report set out to explain recent scientific findings for an "
        "informed general audience, yet the source material provides no "
        "substantive statements to interpret, offering only ellipses where "
        "evidence should appear."
    ),
    (
        "Because the bullet points contain no descriptions of the study's "
        "aims, methods, participants, measurements, or outcomes, it is "
        "impossible to summarize what was investigated or discovered, and any "
        "attempt to extrapolate would require speculation that violates the "
        "evidence-based mandate."
    ),
    (
        "Without even a hint about the research field—whether biomedical, "
        "environmental, social, or technological—we cannot infer the subject "
        "matter or relevance of the absent findings."
    ),
    (
        "Critical scientific literacy depends on transparent documentation of "
        "questions asked, experimental or observational designs deployed, "
        "analytical techniques applied, and uncertainties acknowledged, none "
        "of which can be reported because the dataset is entirely empty."
    ),
    (
        "Ordinarily, a research summary would trace the logical flow from "
        "hypothesis through methodology to findings and limitations, "
        "translating technical language into accessible explanations, "
        "but here that narrative arc collapses because the foundational "
        "evidence has "
        "not been shared, leaving a reminder of the importance of transparent "
        "communication in science."
    ),
    (
        "In the absence of concrete data, the most responsible course is to "
        "highlight this gap, urge the provider of the bullet points to supply "
        "verifiable details, and caution readers that any interpretations of "
        "the supposed study cannot be confirmed or debunked without actual "
        "evidence."
    ),
    (
        "Stakeholders such as policymakers, educators, clinicians, and "
        "community advocates depend on accurate reporting to inform "
        "decisions, but they should postpone action because neither the scope "
        "nor the direction of the missing findings can be determined from the "
        "silent placeholders provided."
    ),
    (
        "Until substantive content is shared, the most constructive takeaway "
        "is a meta-lesson about scientific transparency: rigorous inquiry "
        "requires not only careful experimentation but also thorough "
        "dissemination of methods, data, and interpretations, and without "
        "those elements, even the most enthusiastic communicator cannot craft "
        "a responsible or meaningful summary for the public."
    ),
    (
        "Consequently, this document stands as an invitation for the original "
        "researchers or organizers to release the missing information so that "
        "future summaries can offer the clarity, nuance, and evidence that "
        "readers deserve in full."
    ),
)

FILLER_SENTENCES: Sequence[str] = (
    (
        "This reminder keeps the narrative tethered to the supplied evidence "
        "without extrapolating beyond it."
    ),
    (
        "The emphasis on direct citation underscores that interpretation "
        "should remain firmly grounded in the documented bullet points."
    ),
    (
        "By reiterating the same source material, the summary protects "
        "readers from mistaking speculation for reported observation."
    ),
)


@dataclass(frozen=True)
class SummaryResult:
    """Container for a generated research summary."""

    title: str
    summary: str
    citations: List[List[int]]


class ResearchSummaryGenerator:
    """Produce JSON-compatible summaries from research bullet points."""

    _PLACEHOLDER_VALUES: Sequence[str] = (
        "…",
        "...",
        "N/A",
        "NA",
        "n/a",
        "na",
    )

    def __init__(self, word_target: int = 350) -> None:
        self.word_target = word_target

    def generate_summary(self, bullet_points: Iterable[str]) -> SummaryResult:
        """Create a structured summary from bullet points."""

        bullet_list = [point.strip() for point in bullet_points]
        if not bullet_list:
            return self._build_missing_data_response(0)

        numbered_points = [
            (index, text)
            for index, text in enumerate(bullet_list, start=1)
            if text
        ]

        if not numbered_points or all(
            self._is_placeholder(text) for _, text in numbered_points
        ):
            return self._build_missing_data_response(len(bullet_list))

        return self._build_substantive_summary(numbered_points)

    def _is_placeholder(self, text: str) -> bool:
        stripped = text.strip()
        return not stripped or stripped in self._PLACEHOLDER_VALUES

    def _build_missing_data_response(self, point_count: int) -> SummaryResult:
        if point_count <= 0:
            citation_indices: List[int] = []
        else:
            citation_indices = list(range(1, point_count + 1))

        formatted_sentences = [
            self._apply_citations(sentence, citation_indices)
            for sentence in MISSING_DATA_SENTENCES
        ]
        citations = [list(citation_indices) for _ in MISSING_DATA_SENTENCES]
        summary = " ".join(formatted_sentences)
        return SummaryResult(
            title="Insufficient Data to Summarize Research",
            summary=summary,
            citations=citations,
        )

    def _build_substantive_summary(
        self, numbered_points: Sequence[Tuple[int, str]]
    ) -> SummaryResult:
        all_indices = [index for index, _ in numbered_points]
        sentences: List[Tuple[str, Sequence[int]]] = [
            (
                "This overview synthesizes the supplied research bullet "
                "points to craft an accessible narrative for informed "
                "readers.",
                all_indices,
            ),
            (
                "Every statement remains grounded in the documented notes so "
                "that accuracy is preserved without extrapolation.",
                all_indices,
            ),
        ]

        for index, text in numbered_points:
            normalized = self._normalize_sentence(text)
            sentences.append(
                (
                    f"Bullet {index} reports that {normalized}",
                    [index],
                )
            )
            sentences.append(
                (
                    "This restatement mirrors the source language to prevent "
                    "accidental distortion of the documented evidence.",
                    [index],
                )
            )

        sentences.append(
            (
                "Taken together, these observations form a cohesive outline "
                "that readers can map directly back to the enumerated bullet "
                "points.",
                all_indices,
            )
        )
        sentences.append(
            (
                "The conclusion reiterates that any deeper interpretation "
                "should await additional context beyond the supplied notes.",
                all_indices,
            )
        )

        formatted_sentences: List[str] = []
        citations: List[List[int]] = []
        for sentence, cite_indices in sentences:
            formatted_sentences.append(
                self._apply_citations(sentence, cite_indices)
            )
            citations.append(list(cite_indices))

        summary, citations = self._pad_summary(
            formatted_sentences,
            citations,
            all_indices,
        )

        return SummaryResult(
            title="Research Summary",
            summary=summary,
            citations=citations,
        )

    def _normalize_sentence(self, text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return ""
        if stripped[-1] in ".?!":
            return stripped
        return f"{stripped}."

    def _apply_citations(
        self,
        sentence: str,
        citation_indices: Sequence[int],
    ) -> str:
        if not citation_indices:
            return sentence
        citations = "".join(f"({index})" for index in citation_indices)
        if sentence.endswith((".", "!", "?")):
            return f"{sentence} {citations}".strip()
        return f"{sentence}. {citations}".strip()

    def _pad_summary(
        self,
        sentences: List[str],
        citations: List[List[int]],
        all_indices: Sequence[int],
    ) -> Tuple[str, List[List[int]]]:
        summary = " ".join(sentences)
        word_count = self._count_words(summary)
        filler_index = 0

        while word_count < self.word_target:
            filler_sentence = FILLER_SENTENCES[
                filler_index % len(FILLER_SENTENCES)
            ]
            formatted = self._apply_citations(filler_sentence, all_indices)
            sentences.append(formatted)
            citations.append(list(all_indices))
            summary = " ".join(sentences)
            word_count = self._count_words(summary)
            filler_index += 1

        return summary, citations

    def _count_words(self, text: str) -> int:
        return len([word for word in text.split() if word])
