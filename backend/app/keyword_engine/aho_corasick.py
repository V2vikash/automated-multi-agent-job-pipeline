import re
from collections import deque
from typing import List, Dict, Set, Tuple, Optional
from pydantic import BaseModel, Field
from app.keyword_engine.dictionary import TECH_KEYWORD_DICTIONARY
from app.keyword_engine.normalizer import normalizer


class ExtractedKeyword(BaseModel):
    """Structured keyword item produced by Aho-Corasick engine."""
    keyword: str
    normalized_keyword: str
    category: str
    confidence: float = 1.0


class TrieNode:
    """Trie node used for building Aho-Corasick automaton."""

    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.fail: Optional[TrieNode] = None
        self.output: List[str] = []


class AhoCorasickAutomaton:
    """
    Deterministic Aho-Corasick Automaton for high-speed linear $O(N + M)$
    keyword extraction across job postings.
    """

    def __init__(self):
        self.root = TrieNode()
        self.is_built = False

    def add_pattern(self, pattern: str):
        """Insert pattern into Trie structure."""
        if not pattern:
            return
        node = self.root
        for char in pattern.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.output.append(pattern.lower())
        self.is_built = False

    def build_failure_links(self):
        """Construct failure links using Breadth-First Search (BFS)."""
        queue = deque()

        # Direct children of root have fail link set to root
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                queue.append(child)
                fail_node = current.fail

                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail

                child.fail = fail_node.children[char] if fail_node else self.root
                # Merge outputs from failure link
                child.output.extend(child.fail.output)

        self.is_built = True

    def search(self, text: str) -> List[ExtractedKeyword]:
        """
        Search input text for registered patterns deterministically.
        Validates word boundaries and maps aliases to canonical forms.
        """
        if not self.is_built:
            self.build_failure_links()

        if not text:
            return []

        normalized_text = normalizer.normalize_text(text)
        node = self.root
        found_matches: List[Tuple[int, int, str]] = []  # (start, end, pattern)

        for i, char in enumerate(normalized_text):
            while node is not None and char not in node.children:
                node = node.fail
            if node is None:
                node = self.root
                continue
            node = node.children[char]

            for pattern in node.output:
                start_idx = i - len(pattern) + 1
                end_idx = i + 1

                # Word boundary check to avoid matching 'go' in 'algorithm' or 'js' in 'json'
                if self._is_word_boundary(normalized_text, start_idx, end_idx, pattern):
                    found_matches.append((start_idx, end_idx, pattern))

        # Deduplicate matches and resolve canonical forms
        seen_canonical: Set[str] = set()
        results: List[ExtractedKeyword] = []

        # Sort matches by length descending so longer matching phrases take precedence
        found_matches.sort(key=lambda m: (m[1] - m[0]), reverse=True)

        for start, end, pattern in found_matches:
            canonical, category = normalizer.resolve_canonical(pattern)
            norm_key = canonical.lower()

            if norm_key not in seen_canonical:
                seen_canonical.add(norm_key)
                results.append(ExtractedKeyword(
                    keyword=canonical,
                    normalized_keyword=norm_key,
                    category=category,
                    confidence=1.0
                ))

        return results

    def _is_word_boundary(self, text: str, start: int, end: int, pattern: str) -> bool:
        """Enforce strict word boundaries for short alpha patterns."""
        # For patterns containing symbols like 'c++', 'c#', 'node.js', skip strict word boundary check
        if any(c in pattern for c in ["+", "#", ".", "-"]):
            return True

        # Check character before start
        if start > 0:
            char_before = text[start - 1]
            if char_before.isalnum() or char_before == "_":
                return False

        # Check character after end
        if end < len(text):
            char_after = text[end]
            if char_after.isalnum() or char_after == "_":
                return False

        return True


# Global default instance loaded with dictionary patterns
keyword_automaton = AhoCorasickAutomaton()
for raw_pattern in TECH_KEYWORD_DICTIONARY.keys():
    keyword_automaton.add_pattern(raw_pattern)
keyword_automaton.build_failure_links()
