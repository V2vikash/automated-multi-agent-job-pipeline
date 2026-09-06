import time
import pytest
from app.keyword_engine.aho_corasick import AhoCorasickAutomaton, keyword_automaton


def test_single_and_multiple_keyword_matches():
    """Test extracting single and multiple keywords from text."""
    sample_text = "We build high performance microservices using Python and FastAPI backed by PostgreSQL."
    keywords = keyword_automaton.search(sample_text)

    names = {k.keyword for k in keywords}
    assert "Python" in names
    assert "FastAPI" in names
    assert "PostgreSQL" in names


def test_alias_normalization():
    """Test mapping raw aliases to canonical forms."""
    sample_text = "Experienced in JS, TS, Postgres, Docker, and K8s."
    keywords = keyword_automaton.search(sample_text)

    names = {k.keyword for k in keywords}
    assert "JavaScript" in names
    assert "TypeScript" in names
    assert "PostgreSQL" in names
    assert "Docker" in names
    assert "Kubernetes" in names


def test_punctuation_and_special_character_keywords():
    """Test keywords containing symbols like C++, C#, Node.js, Next.js."""
    sample_text = "Required technologies: C++, C#, Node.js, and Next.js."
    keywords = keyword_automaton.search(sample_text)

    names = {k.keyword for k in keywords}
    assert "C++" in names
    assert "C#" in names
    assert "Node.js" in names
    assert "Next.js" in names


def test_word_boundary_false_positives():
    """Verify short words are not matched inside unrelated larger words."""
    # 'go' should not match inside 'algorithm' or 'category'
    sample_text = "We optimize backend algorithms and category pages."
    keywords = keyword_automaton.search(sample_text)

    names = {k.keyword for k in keywords}
    assert "Go" not in names


def test_empty_and_duplicate_inputs():
    """Verify empty input returns empty list and duplicates are prevented."""
    assert keyword_automaton.search("") == []
    assert keyword_automaton.search(None) == []

    text_with_dups = "Python Python python PYTHON fastAPI FastAPI"
    keywords = keyword_automaton.search(text_with_dups)
    names = [k.keyword for k in keywords]
    assert names.count("Python") == 1
    assert names.count("FastAPI") == 1


def test_aho_corasick_performance_benchmark():
    """Benchmark Aho-Corasick linear speed over large job description text."""
    large_text = "We are seeking a Lead Backend Engineer with expertise in " + ", ".join([
        "Python", "FastAPI", "PostgreSQL", "Apache Kafka", "Redis", "Docker", "Kubernetes",
        "React", "TypeScript", "AWS", "Terraform", "LangGraph", "Pytest", "Go", "C++"
    ]) * 100

    start_time = time.perf_counter()
    keywords = keyword_automaton.search(large_text)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert len(keywords) >= 10
    assert elapsed_ms < 50.0  # Must complete in under 50 milliseconds
