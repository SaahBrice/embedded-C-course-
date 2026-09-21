from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
from ..models import Attempt, CheckResult, CheckSpec, Mission


_OUTPUT_LIMIT = 100_000
_SUPPORTED_TYPES = frozenset({
    "file_exists", "text_regex", "markdown_response", "command", "c_harness",
    "c_program", "c_test_pair", "project_harness", "manual_evidence",
})


class CheckerRegistry:
    """Runs the small, allow-listed set of declarative mission checks."""

    def __init__(self, repository_root: Path):
        self.repository_root = repository_root.resolve()

    def configuration_issue(self, spec: CheckSpec, mission: Mission) -> str | None:
        """Return a static authoring problem without executing learner-controlled work."""
        if spec.type not in _SUPPORTED_TYPES:
            return f"unsupported checker type {spec.type!r}"
        try:
            if spec.type in {"file_exists", "text_regex", "markdown_response"}:
                self._relative_config_path(spec.config["path"], "path")
            if spec.type == "text_regex":
                pattern = spec.config["pattern"]
                if not isinstance(pattern, str):
                    raise TypeError("pattern must be a string")
                re.compile(pattern)
            elif spec.type == "markdown_response":
                self._validate_markdown_config(spec.config)
            elif spec.type == "command":
                self._validate_command_config(spec.config)
            elif spec.type == "c_harness":
                self._validate_c_build_config(spec.config, "sources")
                self._validate_mission_file(mission, spec.config["harness"], "harness")
                for source in self._path_list(spec.config.get("support_sources", []), "support_sources", allow_empty=True):
                    path = (self.repository_root / source).resolve()
                    if self.repository_root not in path.parents or not path.is_file():
                        raise ValueError(f"support source must be an existing repository file: {source}")
                for include in self._path_list(spec.config.get("support_include_dirs", []), "support_include_dirs", allow_empty=True):
                    path = (self.repository_root / include).resolve()
                    if self.repository_root not in path.parents or not path.is_dir():
                        raise ValueError(f"support include must be an existing repository directory: {include}")
            elif spec.type == "c_program":
                self._validate_c_build_config(spec.config, "sources")
                if not isinstance(spec.config["expected_stdout"], str):
                    raise TypeError("expected_stdout must be a string")
                expected_exit = spec.config["expected_exit"]
                if not isinstance(expected_exit, int) or isinstance(expected_exit, bool) or not 0 <= expected_exit <= 255:
                    raise ValueError("expected_exit must be between 0 and 255")
                if not isinstance(spec.config.get("stdin", ""), str):
                    raise TypeError("stdin must be a string")
                self._string_list(spec.config.get("args", []), "args", allow_empty=True)
            elif spec.type == "c_test_pair":
                self._validate_c_build_config(spec.config, "test_sources")
                self._validate_mission_file(mission, spec.config["good_source"], "good_source")
                self._validate_mission_file(mission, spec.config["defective_source"], "defective_source")
            elif spec.type == "project_harness":
                self._validate_mission_file(mission, spec.config["harness"], "harness")
                self._validate_timeout(spec.config.get("timeout", 20))
            elif spec.type == "manual_evidence":
                self._relative_config_path(spec.config["path"], "path")
                fields = self._string_list(spec.config["required_fields"], "required_fields")
                if len(set(fields)) != len(fields):
                    raise ValueError("required_fields must not contain duplicates")
        except (KeyError, TypeError, ValueError, re.error) as exc:
            return f"invalid {spec.type} configuration: {exc}"
        return None

    @staticmethod
    def _validate_markdown_config(config: dict[str, object]) -> None:
        headings = config["headings"]
        minimum_words = config["minimum_words"]
        if not isinstance(headings, list) or not headings or not all(
            isinstance(item, str) and item.strip() for item in headings
        ):
            raise TypeError("headings must be a non-empty array of strings")
        for name, value in (
            ("minimum_words", minimum_words),
            ("minimum_section_words", config.get("minimum_section_words", 1)),
            ("minimum_unique_words", config.get("minimum_unique_words", 1)),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 10000:
                raise ValueError(f"{name} must be between 1 and 10000")
        maximum = config.get("maximum_word_fraction", 1.0)
        if not isinstance(maximum, (int, float)) or isinstance(maximum, bool) or not 0 < maximum <= 1:
            raise ValueError("maximum_word_fraction must be greater than 0 and at most 1")
        groups = config.get("required_concept_groups", [])
        if (
            not isinstance(groups, list)
            or ("required_concept_groups" in config and not groups)
            or not all(
            isinstance(group, list)
            and group
            and all(isinstance(term, str) and term.strip() for term in group)
            for group in groups
            )
        ):
            raise TypeError("required_concept_groups must be an array of non-empty string arrays")

    @staticmethod
    def _relative_config_path(value: object, field: str) -> Path:
        if not isinstance(value, str):
            raise TypeError(f"{field} must be a string")
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"{field} must be a safe relative path")
        return path

    @classmethod
    def _path_list(cls, value: object, field: str, *, allow_empty: bool = False) -> list[Path]:
        strings = cls._string_list(value, field, allow_empty=allow_empty)
        return [cls._relative_config_path(item, field) for item in strings]

    @staticmethod
    def _string_list(value: object, field: str, *, allow_empty: bool = False) -> list[str]:
        if (
            not isinstance(value, list)
            or (not allow_empty and not value)
            or not all(isinstance(item, str) and item for item in value)
        ):
            qualifier = "an array" if allow_empty else "a non-empty array"
            raise TypeError(f"{field} must be {qualifier} of strings")
        return value

    @classmethod
    def _validate_c_build_config(cls, config: dict[str, object], source_field: str) -> None:
        cls._path_list(config[source_field], source_field)
        flags = config.get("cflags", [])
        cls._string_list(flags, "cflags", allow_empty=True)
        compiler = config.get("compiler", "cc")
        if not isinstance(compiler, str) or not compiler:
            raise TypeError("compiler must be a non-empty string")
        cls._validate_timeout(config.get("timeout", 20))

    @classmethod
    def _validate_mission_file(cls, mission: Mission, value: object, field: str) -> Path:
        relative = cls._relative_config_path(value, field)
        path = (mission.root / relative).resolve()
        if mission.root not in path.parents or not path.is_file():
            raise ValueError(f"{field} must be an existing file inside the mission package")
        return path

    @classmethod
    def _validate_command_config(cls, config: dict[str, object]) -> None:
        argv = config["argv"]
        if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) for arg in argv):
            raise TypeError("argv must be a non-empty array of strings")
        cls._validate_timeout(config.get("timeout", 10))

    @staticmethod
    def _validate_timeout(timeout: object) -> None:
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0 or timeout > 120:
            raise ValueError("timeout must be greater than 0 and at most 120 seconds")

    def run(
        self, spec: CheckSpec, attempt: Attempt, mission: Mission | None = None,
    ) -> CheckResult:
        handlers = {
            "file_exists": self._file_exists,
            "text_regex": self._text_regex,
            "markdown_response": self._markdown_response,
            "command": self._command,
        }
        mission_handlers = {
            "c_harness": self._c_harness,
            "c_test_pair": self._c_test_pair,
            "project_harness": self._project_harness,
        }
        if spec.type in mission_handlers:
            try:
                return mission_handlers[spec.type](spec, attempt, mission)
            except (KeyError, TypeError, ValueError) as exc:
                return self._configuration(spec, f"invalid {spec.type} configuration: {exc}")
        if spec.type == "c_program":
            handler = self._c_program
        elif spec.type == "manual_evidence":
            handler = self._manual_evidence
        else:
            handler = handlers.get(spec.type)
        if handler is None:
            return self._configuration(spec, f"unsupported checker type {spec.type!r}")
        try:
            return handler(spec, attempt)
        except (KeyError, TypeError, ValueError) as exc:
            return self._configuration(spec, f"invalid {spec.type} configuration: {exc}")

    def _safe_attempt_path(self, attempt: Attempt, value: object) -> Path:
        if not isinstance(value, str):
            raise TypeError("path must be a string")
        candidate = (attempt.path / value).resolve()
        if candidate != attempt.path and attempt.path not in candidate.parents:
            raise ValueError("path escapes the attempt workspace")
        return candidate

    def _file_exists(self, spec: CheckSpec, attempt: Attempt) -> CheckResult:
        path = self._safe_attempt_path(attempt, spec.config["path"])
        if path.is_file():
            return self._pass(spec, f"found {path.relative_to(attempt.path)}")
        return self._fail(spec, f"missing required file: {path.relative_to(attempt.path)}")

    def _text_regex(self, spec: CheckSpec, attempt: Attempt) -> CheckResult:
        path = self._safe_attempt_path(attempt, spec.config["path"])
        pattern = spec.config["pattern"]
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        if not path.is_file():
            return self._fail(spec, f"missing required file: {path.relative_to(attempt.path)}")
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return self._configuration(spec, f"cannot read {path.name}: {exc}")
        try:
            matched = re.search(pattern, content, re.MULTILINE | re.DOTALL) is not None
        except re.error as exc:
            return self._configuration(spec, f"invalid regular expression: {exc}")
        if matched:
            return self._pass(spec, f"{path.name} contains the required pattern")
        return self._fail(spec, f"{path.name} does not contain the required pattern")

    def _markdown_response(self, spec: CheckSpec, attempt: Attempt) -> CheckResult:
        path = self._safe_attempt_path(attempt, spec.config["path"])
        self._validate_markdown_config(spec.config)
        headings = spec.config["headings"]
        minimum_words = spec.config["minimum_words"]
        if not path.is_file():
            return self._fail(spec, f"missing required file: {path.relative_to(attempt.path)}")
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return self._configuration(spec, f"cannot read {path.name}: {exc}")
        heading_matches = list(re.finditer(r"^#{1,6}\s+(.+?)\s*$", content, re.MULTILINE))
        sections: dict[str, str] = {}
        for index, match in enumerate(heading_matches):
            name = match.group(1).strip()
            end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(content)
            sections[name.casefold()] = content[match.end():end]
        missing = [heading for heading in headings if heading.casefold() not in sections]
        if missing:
            return self._fail(spec, f"{path.name} is missing sections: {', '.join(missing)}")
        minimum_section_words = spec.config.get("minimum_section_words", 1)
        for heading in headings:
            count = len(re.findall(r"\b[\w'-]+\b", sections[heading.casefold()]))
            if count < minimum_section_words:
                return self._fail(
                    spec, f"section {heading!r} needs {minimum_section_words} words; found {count}"
                )
        body = "\n".join(sections[heading.casefold()] for heading in headings)
        words = [word.casefold() for word in re.findall(r"\b[\w'-]+\b", body)]
        word_count = len(words)
        if word_count < minimum_words:
            return self._fail(spec, f"{path.name} needs {minimum_words} words; found {word_count}")
        unique_count = len(set(words))
        minimum_unique = spec.config.get("minimum_unique_words", 1)
        if unique_count < minimum_unique:
            return self._fail(
                spec, f"{path.name} needs {minimum_unique} unique words; found {unique_count}"
            )
        maximum_fraction = float(spec.config.get("maximum_word_fraction", 1.0))
        if words:
            most_common_count = max(words.count(word) for word in set(words))
            if most_common_count / word_count > maximum_fraction:
                return self._fail(spec, f"{path.name} repeats one word too frequently")
        folded = content.casefold()
        for group in spec.config.get("required_concept_groups", []):
            if not any(
                re.search(rf"(?<!\w){re.escape(term.casefold())}(?!\w)", folded)
                for term in group
            ):
                return self._fail(spec, f"{path.name} is missing a required concept group")
        return self._pass(spec, f"{path.name} contains the required analysis ({word_count} words)")

    def _c_harness(self, spec: CheckSpec, attempt: Attempt, mission: Mission | None) -> CheckResult:
        if mission is None:
            raise ValueError("mission context is required")
        issue = self.configuration_issue(spec, mission)
        if issue is not None:
            return self._configuration(spec, issue)
        with tempfile.TemporaryDirectory(prefix=f"learn-check-{mission.id}-") as tmp:
            temporary = Path(tmp)
            learner = temporary / "learner"
            self._copy_learner_tree(attempt, learner)
            sources = [learner / path for path in self._path_list(spec.config["sources"], "sources")]
            for source in sources:
                if not source.is_file():
                    return self._fail(spec, f"missing learner source: {source.relative_to(learner)}")
            immutable = temporary / "immutable"
            harness_source = self._validate_mission_file(mission, spec.config["harness"], "harness")
            harness = immutable / "harness" / harness_source.name
            self._copy_file(harness_source, harness)
            support_sources: list[Path] = []
            for relative in self._path_list(spec.config.get("support_sources", []), "support_sources", allow_empty=True):
                copied = immutable / "repository" / relative
                self._copy_file(self.repository_root / relative, copied)
                support_sources.append(copied)
            include_dirs: list[Path] = []
            for index, relative in enumerate(self._path_list(
                spec.config.get("support_include_dirs", []), "support_include_dirs", allow_empty=True
            )):
                copied = immutable / "includes" / f"{index:03d}"
                self._copy_directory(self.repository_root / relative, copied)
                include_dirs.append(copied)
            executable = temporary / "mission-test"
            cflags, compiler, timeout = self._c_build_options(spec.config)
            argv = [
                compiler, *cflags, "-I", str(learner),
                *(part for include in include_dirs for part in ("-I", str(include))),
                *map(str, sources), *map(str, support_sources), str(harness),
                "-o", str(executable),
            ]
            compiled = self._execute(spec, argv, temporary, timeout)
            if not compiled.passed:
                return CheckResult(
                    spec.id, spec.name, False, compiled.category,
                    f"learner source did not build: {compiled.message}",
                    compiled.stdout, compiled.stderr, compiled.exit_code,
                )
            ran = self._execute(spec, [str(executable)], temporary, timeout)
            if not ran.passed:
                return CheckResult(
                    spec.id, spec.name, False, ran.category,
                    f"immutable mission tests failed: {ran.message}",
                    ran.stdout, ran.stderr, ran.exit_code,
                )
            return CheckResult(
                spec.id, spec.name, True, "passed", "learner source passed immutable mission tests",
                ran.stdout, ran.stderr, 0,
            )

    def _c_program(self, spec: CheckSpec, attempt: Attempt) -> CheckResult:
        self._validate_c_build_config(spec.config, "sources")
        if not isinstance(spec.config["expected_stdout"], str):
            raise TypeError("expected_stdout must be a string")
        expected_exit = spec.config["expected_exit"]
        if not isinstance(expected_exit, int) or isinstance(expected_exit, bool) or not 0 <= expected_exit <= 255:
            raise ValueError("expected_exit must be between 0 and 255")
        stdin = spec.config.get("stdin", "")
        if not isinstance(stdin, str):
            raise TypeError("stdin must be a string")
        args = self._string_list(spec.config.get("args", []), "args", allow_empty=True)
        with tempfile.TemporaryDirectory(prefix="learn-program-") as tmp:
            temporary = Path(tmp)
            learner = temporary / "learner"
            self._copy_learner_tree(attempt, learner)
            sources = [learner / path for path in self._path_list(spec.config["sources"], "sources")]
            for source in sources:
                if not source.is_file():
                    return self._fail(spec, f"missing learner source: {source.relative_to(learner)}")
            executable = temporary / "program"
            cflags, compiler, timeout = self._c_build_options(spec.config)
            compiled = self._execute(
                spec, [compiler, *cflags, *map(str, sources), "-o", str(executable)],
                temporary, timeout,
            )
            if not compiled.passed:
                return CheckResult(
                    spec.id, spec.name, False, compiled.category,
                    f"learner program did not build: {compiled.message}",
                    compiled.stdout, compiled.stderr, compiled.exit_code,
                )
            ran = self._execute(spec, [str(executable), *args], temporary, timeout, stdin=stdin)
            if ran.category in {"timeout", "missing_tool", "engine_error"}:
                return ran
            if ran.exit_code != expected_exit:
                return self._fail_with_output(
                    spec, f"program exited with {ran.exit_code}; expected {expected_exit}", ran
                )
            if ran.stdout != spec.config["expected_stdout"]:
                return self._fail_with_output(spec, "program stdout did not exactly match expected output", ran)
            return CheckResult(
                spec.id, spec.name, True, "passed", "program output and exit status matched exactly",
                ran.stdout, ran.stderr, 0,
            )

    def _c_test_pair(self, spec: CheckSpec, attempt: Attempt, mission: Mission | None) -> CheckResult:
        if mission is None:
            raise ValueError("mission context is required")
        issue = self.configuration_issue(spec, mission)
        if issue is not None:
            return self._configuration(spec, issue)
        with tempfile.TemporaryDirectory(prefix=f"learn-test-pair-{mission.id}-") as tmp:
            temporary = Path(tmp)
            learner = temporary / "learner"
            self._copy_learner_tree(attempt, learner)
            tests = [learner / path for path in self._path_list(spec.config["test_sources"], "test_sources")]
            for source in tests:
                if not source.is_file():
                    return self._fail(spec, f"missing learner test source: {source.relative_to(learner)}")
            cflags, compiler, timeout = self._c_build_options(spec.config)
            copied: dict[str, Path] = {}
            for key in ("good_source", "defective_source"):
                source = self._validate_mission_file(mission, spec.config[key], key)
                copied[key] = temporary / "immutable" / key / source.name
                self._copy_file(source, copied[key])
            outcomes: dict[str, CheckResult] = {}
            for key in ("good_source", "defective_source"):
                executable = temporary / key
                compiled = self._execute(
                    spec, [compiler, *cflags, "-I", str(learner), *map(str, tests), str(copied[key]), "-o", str(executable)],
                    temporary, timeout,
                )
                if not compiled.passed:
                    category = compiled.category if key == "good_source" else "configuration_error"
                    return CheckResult(
                        spec.id, spec.name, False, category,
                        f"test pair did not build with {key}: {compiled.message}",
                        compiled.stdout, compiled.stderr, compiled.exit_code,
                    )
                outcomes[key] = self._execute(spec, [str(executable)], temporary, timeout)
            if not outcomes["good_source"].passed:
                return self._fail_with_output(spec, "learner tests rejected the good implementation", outcomes["good_source"])
            defective = outcomes["defective_source"]
            if defective.category in {"timeout", "missing_tool", "engine_error"}:
                return defective
            if defective.exit_code == 0:
                return self._fail_with_output(spec, "learner tests did not detect the defective implementation", defective)
            return self._pass(spec, "learner tests passed the good source and rejected the defective source")

    def _project_harness(self, spec: CheckSpec, attempt: Attempt, mission: Mission | None) -> CheckResult:
        if mission is None:
            raise ValueError("mission context is required")
        issue = self.configuration_issue(spec, mission)
        if issue is not None:
            return self._configuration(spec, issue)
        timeout = spec.config.get("timeout", 20)
        with tempfile.TemporaryDirectory(prefix=f"learn-project-{mission.id}-") as tmp:
            temporary = Path(tmp)
            learner = temporary / "learner"
            build = temporary / "build"
            self._copy_learner_tree(attempt, learner)
            build.mkdir()
            source = self._validate_mission_file(mission, spec.config["harness"], "harness")
            harness = temporary / "immutable" / source.name
            self._copy_file(source, harness)
            ran = self._execute(
                spec, [sys.executable, str(harness), str(learner), str(build)], build, timeout
            )
            if not ran.passed:
                return CheckResult(
                    spec.id, spec.name, False, ran.category,
                    f"project harness failed: {ran.message}", ran.stdout, ran.stderr, ran.exit_code,
                )
            return CheckResult(
                spec.id, spec.name, True, "passed", "project passed the trusted mission harness",
                ran.stdout, ran.stderr, 0,
            )

    def _manual_evidence(self, spec: CheckSpec, attempt: Attempt) -> CheckResult:
        path = self._safe_attempt_path(attempt, spec.config["path"])
        fields = self._string_list(spec.config["required_fields"], "required_fields")
        if not path.is_file():
            return self._fail(spec, f"missing manual evidence file: {path.relative_to(attempt.path)}")
        try:
            evidence = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return self._fail(spec, f"manual evidence must be valid JSON: {exc}")
        if not isinstance(evidence, dict):
            return self._fail(spec, "manual evidence must be a JSON object")
        missing = [field for field in fields if not self._evidence_value_present(evidence.get(field))]
        if missing:
            return self._fail(spec, f"manual evidence needs non-empty fields: {', '.join(missing)}")
        return self._pass(
            spec, "structured self-attestation recorded; physical behavior was not machine-verified"
        )

    @staticmethod
    def _evidence_value_present(value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, dict)):
            return bool(value)
        return value is not None

    @staticmethod
    def _copy_file(source: Path, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    @staticmethod
    def _copy_directory(source: Path, destination: Path) -> None:
        for item in source.rglob("*"):
            if item.is_symlink():
                raise ValueError(f"immutable support contains a symlink: {item}")
        shutil.copytree(source, destination)

    @classmethod
    def _copy_learner_tree(cls, attempt: Attempt, destination: Path) -> None:
        """Copy inputs to reduce accidental path exposure; this is not hostile-code containment."""
        for item in attempt.path.rglob("*"):
            if item.is_symlink():
                raise ValueError(f"learner workspace contains a symlink: {item.name}")
        shutil.copytree(attempt.path, destination)

    @staticmethod
    def _c_build_options(config: dict[str, object]) -> tuple[list[str], str, int | float]:
        cflags = config.get(
            "cflags", ["-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O0", "-g"]
        )
        compiler = config.get("compiler", "cc")
        timeout = config.get("timeout", 20)
        return cflags, compiler, timeout

    @staticmethod
    def _fail_with_output(spec: CheckSpec, message: str, result: CheckResult) -> CheckResult:
        return CheckResult(
            spec.id, spec.name, False, "learner_failure", message,
            result.stdout, result.stderr, result.exit_code,
        )

    def _command(self, spec: CheckSpec, attempt: Attempt) -> CheckResult:
        argv = spec.config["argv"]
        if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) for arg in argv):
            raise TypeError("argv must be a non-empty array of strings")
        timeout = spec.config.get("timeout", 10)
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0 or timeout > 120:
            raise ValueError("timeout must be greater than 0 and at most 120 seconds")
        replacements = {
            "{attempt}": str(attempt.path),
            "{repo}": str(self.repository_root),
        }
        expanded = [replacements.get(arg, arg) for arg in argv]
        env = os.environ.copy()
        env.update({
            "LEARN_ATTEMPT": str(attempt.path),
            "LEARN_REPOSITORY": str(self.repository_root),
        })
        return self._execute(spec, expanded, attempt.path, timeout, environment=env)

    def _execute(
        self,
        spec: CheckSpec,
        argv: list[str],
        cwd: Path,
        timeout: int | float,
        *,
        stdin: str | None = None,
        environment: dict[str, str] | None = None,
    ) -> CheckResult:
        # Temp-build checkers deliberately remove convenience path exports. Copying inputs
        # reduces accidental repository exposure; it is not containment for hostile code.
        env = os.environ.copy() if environment is None else environment
        if environment is None:
            env.pop("LEARN_ATTEMPT", None)
            env.pop("LEARN_REPOSITORY", None)
        try:
            process = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                stdin=subprocess.PIPE if stdin is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
        except FileNotFoundError:
            return CheckResult(
                spec.id, spec.name, False, "missing_tool",
                f"required tool is not installed or not on PATH: {argv[0]}",
            )
        except OSError as exc:
            return CheckResult(spec.id, spec.name, False, "engine_error", f"cannot launch check: {exc}")
        try:
            stdout, stderr = process.communicate(input=stdin, timeout=float(timeout))
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
            return CheckResult(
                spec.id, spec.name, False, "timeout",
                f"check timed out after {timeout:g} seconds", stdout[-_OUTPUT_LIMIT:], stderr[-_OUTPUT_LIMIT:],
            )
        stdout = stdout[-_OUTPUT_LIMIT:]
        stderr = stderr[-_OUTPUT_LIMIT:]
        if process.returncode == 0:
            return CheckResult(
                spec.id, spec.name, True, "passed", "command completed successfully",
                stdout, stderr, process.returncode,
            )
        return CheckResult(
            spec.id, spec.name, False, "learner_failure",
            f"command exited with status {process.returncode}", stdout, stderr, process.returncode,
        )

    @staticmethod
    def _pass(spec: CheckSpec, message: str) -> CheckResult:
        return CheckResult(spec.id, spec.name, True, "passed", message, exit_code=0)

    @staticmethod
    def _fail(spec: CheckSpec, message: str) -> CheckResult:
        return CheckResult(spec.id, spec.name, False, "learner_failure", message, exit_code=1)

    @staticmethod
    def _configuration(spec: CheckSpec, message: str) -> CheckResult:
        return CheckResult(spec.id, spec.name, False, "configuration_error", message)
