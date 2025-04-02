from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass
from .parser import ASTParser
import importlib
import logging
from pathlib import Path

@dataclass
class Finding:
    """Represents a code analysis finding."""
    rule: str
    message: str
    severity: str
    line: int
    code_snippet: Optional[str] = None

class CodeAnalyzer:
    """A code analyzer that applies multiple rules to analyze code quality."""
    
    def __init__(self, rule_modules: List[str]):
        """Initialize the analyzer with rule modules.
        
        Args:
            rule_modules: List of module names containing rule functions.
            
        Raises:
            ValueError: If no rule modules are specified.
            ImportError: If a rule module cannot be imported.
            RuntimeError: If there's an error loading rules from a module.
        """
        if not rule_modules:
            raise ValueError("No rule modules specified")
            
        self.logger = logging.getLogger(__name__)
        self.rules = self._load_rules(rule_modules)
        
    def _load_rules(self, modules: List[str]) -> Dict[str, Callable]:
        """Dynamically load rule functions from specified modules.
        
        Args:
            modules: List of module names to load rules from.
            
        Returns:
            Dictionary mapping rule names to their corresponding functions.
            
        Raises:
            ImportError: If a module cannot be imported.
            RuntimeError: If there's an error loading rules from a module.
        """
        rules: Dict[str, Callable] = {}
        
        for module_name in modules:
            try:
                module = importlib.import_module(module_name)
                for rule_name in dir(module):
                    if rule_name.startswith('_'):
                        continue
                        
                    rule = getattr(module, rule_name)
                    if callable(rule):
                        rules[rule_name] = rule
                        
            except ImportError as e:
                self.logger.error(f"Failed to import rule module {module_name}: {e}")
                raise ImportError(f"Failed to import rule module {module_name}: {e}")
            except Exception as e:
                self.logger.error(f"Error loading rules from {module_name}: {e}")
                raise RuntimeError(f"Error loading rules from {module_name}: {e}")
                
        return rules

    def analyze(self, code: str) -> List[Finding]:
        """Perform multi-dimensional code analysis.
        
        Args:
            code: The source code to analyze.
            
        Returns:
            List of Finding objects containing analysis results.
        """
        try:
            ast_parser = ASTParser(code)
        except ValueError as e:
            return [Finding(
                rule='syntax_check',
                message=str(e),
                severity='critical',
                line=0
            )]

        findings: List[Finding] = []
        code_lines = ast_parser.raw_code.splitlines()
        
        # Execute static rule checks
        for rule_name, check_func in self.rules.items():
            try:
                if issues := check_func(ast_parser.tree):
                    findings.extend(
                        Finding(
                            rule=rule_name,
                            message=issue['msg'],
                            severity=issue['level'],
                            line=issue['lineno'],
                            code_snippet=code_lines[issue['lineno']-1] if 0 <= issue['lineno']-1 < len(code_lines) else None
                        )
                        for issue in issues
                    )
            except Exception as e:
                self.logger.error(f"Rule {rule_name} execution failed: {e}")
                findings.append(Finding(
                    rule=rule_name,
                    message=f"Rule execution failed: {e}",
                    severity='error',
                    line=0
                ))
        
        return findings