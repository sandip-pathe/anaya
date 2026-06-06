"""Structural scanner for AST-backed rules."""

from __future__ import annotations

import ast
import re

from anaya.engine.models import Rule, Violation
from anaya.engine.scanners.base import Scanner
from anaya.engine.scanners.pattern import detect_language


class AstScanner(Scanner):
    """Scan source text with structural AST rules."""

    def scan_file_content(
        self,
        file_path: str,
        content: str,
        rules: list[Rule],
    ) -> list[Violation]:
        language = detect_language(file_path)
        if language != "python":
            return []

        ast_rules = [rule for rule in rules if rule.enabled and rule.type == "ast"]
        if not ast_rules:
            return []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        lines = content.splitlines()
        parents = _parent_map(tree)
        violations: list[Violation] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            if isinstance(parents.get(node), ast.ClassDef):
                continue
            for rule in ast_rules:
                if not _rule_applies_to_function(rule, node):
                    continue
                if _function_contains_required_call(rule, node):
                    continue
                violations.append(_build_violation(rule, file_path, node, lines))

        return sorted(violations, key=lambda item: (item.line_number, item.rule_id))


def _rule_applies_to_function(rule: Rule, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    raw_ast = rule.raw.get("ast", {})
    return bool(re.search(str(raw_ast.get("name_matches", "")), node.name, re.IGNORECASE))


def _function_contains_required_call(rule: Rule, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    raw_ast = rule.raw.get("ast", {})
    required_patterns = tuple(str(pattern) for pattern in raw_ast.get("must_contain", ()))
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        call_name = _call_name(child.func)
        if any(re.search(pattern, call_name, re.IGNORECASE) for pattern in required_patterns):
            return True
    return False


def _parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    return parents


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def _build_violation(
    rule: Rule,
    file_path: str,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    lines: list[str],
) -> Violation:
    line_number = node.lineno
    snippet = lines[line_number - 1].rstrip() if line_number <= len(lines) else node.name
    return Violation(
        rule_id=rule.id,
        rule_name=rule.name,
        severity=rule.severity,
        file_path=file_path,
        line_number=line_number,
        end_line=getattr(node, "end_lineno", None),
        column=node.col_offset + 1,
        snippet=snippet,
        message=rule.message.format(line=line_number, file=file_path, function=node.name, rule=rule.id),
        fix_hint=rule.fix_hint,
        references=rule.references,
        pack_id=rule.pack_id,
        confidence=1.0,
    )
