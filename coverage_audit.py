import json
import re
from pathlib import Path
from typing import Dict, List


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _load_config(repo_root: Path) -> Dict:
    config_path = repo_root / "coverage_config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing coverage_config.json at {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def _list_files(base_dir: Path, extensions: List[str]) -> List[Path]:
    return sorted(path for path in base_dir.rglob("*") if path.is_file() and path.suffix.lower() in extensions)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _matches(text: str, keywords: List[str]) -> bool:
    normalized = _normalize(text)
    return any(_normalize(keyword) in normalized for keyword in keywords if keyword)


def _make_paths(path_strings: List[str], base_dir: Path) -> List[Path]:
    paths: List[Path] = []
    for path_str in path_strings:
        candidate = Path(path_str)
        if candidate.is_absolute():
            if candidate.exists():
                paths.append(candidate.resolve())
        else:
            direct = base_dir / path_str
            if direct.exists():
                paths.append(direct.resolve())
            else:
                # Search recursively for the filename
                for p in base_dir.rglob("*"):
                    if p.is_file() and path_str in str(p):
                        paths.append(p.resolve())
    return list(set(paths))


def _find_matches(paths: List[Path], keywords: List[str]) -> List[str]:
    if not keywords:
        return []
    matched: List[str] = []
    for path in paths:
        text = _read_text(path)
        if _matches(text, keywords) or _matches(str(path), keywords):
            matched.append(str(path))
    return matched


def build_coverage_report(repo_root: Path) -> Dict[str, Dict]:
    config = _load_config(repo_root)

    source_dir = Path(config.get("source_dir", ""))
    test_dir = repo_root / config.get("test_dir", "tests")

    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    if not test_dir.exists():
        raise FileNotFoundError(f"Test directory not found: {test_dir}")

    source_files = _list_files(source_dir, [".ts", ".tsx", ".js", ".jsx", ".py"])
    test_files = _list_files(test_dir, [".py"])

    report: Dict[str, Dict] = {
        "source_dir": str(source_dir),
        "test_dir": str(test_dir),
        "source_files": [str(p) for p in source_files],
        "test_files": [str(p) for p in test_files],
        "features": {},
    }

    feature_list = config.get("features", [])
    for feature in feature_list:
        name = feature["name"]
        source_keywords = feature.get("source_keywords", [])
        test_keywords = feature.get("test_keywords", [])
        source_paths = feature.get("source_paths", [])
        test_paths = feature.get("test_paths", [])

        candidate_source_files = _make_paths(source_paths, source_dir) if source_paths else source_files
        candidate_test_files = _make_paths(test_paths, test_dir) if test_paths else test_files

        matched_source = _find_matches(candidate_source_files, source_keywords)
        matched_test = _find_matches(candidate_test_files, test_keywords)

        source_count = len(matched_source)
        test_count = len(matched_test)
        source_presence_pct = 100 if source_count > 0 else 0
        test_presence_pct = 100 if test_count > 0 else 0

        feature_report = {
            "source_matches": matched_source,
            "test_matches": matched_test,
            "source_match_count": source_count,
            "test_match_count": test_count,
            "source_presence_pct": source_presence_pct,
            "test_presence_pct": test_presence_pct,
        }

        actions = feature.get("actions", [])
        if actions:
            covered_actions = 0
            feature_report["actions"] = []
            for action in actions:
                action_name = action.get("name")
                action_source_keywords = action.get("source_keywords", [])
                action_test_keywords = action.get("test_keywords", [])
                action_source_paths = action.get("source_paths", [])
                action_test_paths = action.get("test_paths", [])

                action_source_candidates = _make_paths(action_source_paths, source_dir) if action_source_paths else source_files
                action_test_candidates = _make_paths(action_test_paths, test_dir) if action_test_paths else test_files

                action_source_matches = _find_matches(action_source_candidates, action_source_keywords)
                action_test_matches = _find_matches(action_test_candidates, action_test_keywords)

                if not action_source_matches and not action_test_matches:
                    action_status = "missing_in_both"
                elif not action_source_matches:
                    action_status = "missing_in_source"
                elif not action_test_matches:
                    action_status = "missing_in_automation"
                else:
                    action_status = "covered"
                    covered_actions += 1

                action_source_count = len(action_source_matches)
                action_test_count = len(action_test_matches)
                action_coverage_pct = 100 if action_status == "covered" else 0

                feature_report["actions"].append({
                    "name": action_name,
                    "status": action_status,
                    "source_matches": action_source_matches,
                    "test_matches": action_test_matches,
                    "source_match_count": action_source_count,
                    "test_match_count": action_test_count,
                    "coverage_pct": action_coverage_pct,
                })

            total_actions = len(actions)
            coverage_pct = int(round(100.0 * covered_actions / total_actions)) if total_actions else 0
            feature_report["coverage_pct"] = coverage_pct
            if covered_actions == total_actions:
                status = "covered"
            elif any(a["status"] == "missing_in_automation" for a in feature_report["actions"]):
                status = "missing_in_automation"
            elif any(a["status"] == "missing_in_source" for a in feature_report["actions"]):
                status = "missing_in_source"
            else:
                status = "partial"
            feature_report["status"] = status
        else:
            if not matched_source and not matched_test:
                status = "missing_in_both"
            elif not matched_source:
                status = "missing_in_source"
            elif not matched_test:
                status = "missing_in_automation"
            else:
                status = "covered"
            coverage_pct = 0
            if source_count > 0:
                coverage_pct = int(round(min(100.0, (test_count / float(source_count)) * 100)))
            feature_report["coverage_pct"] = coverage_pct
            feature_report["status"] = status

        report["features"][name] = feature_report

    return report


def print_report(report: Dict[str, Dict]) -> None:
    print("Developer code vs automation coverage report")
    print("=" * 48)
    print(f"Source directory: {report['source_dir']}")
    print(f"Test directory: {report['test_dir']}")
    print(f"Source files discovered: {len(report['source_files'])}")
    print(f"Test files discovered: {len(report['test_files'])}")
    print()

    for feature_name, feature_data in report["features"].items():
        print(f"Feature: {feature_name}")
        print(f"  status: {feature_data['status']}")
        print(f"  source matches: {len(feature_data['source_matches'])}")
        for path in feature_data["source_matches"]:
            print(f"    - {path}")
        print(f"  test matches: {len(feature_data['test_matches'])}")
        for path in feature_data["test_matches"]:
            print(f"    - {path}")
        if feature_data.get("actions"):
            print(f"  actions (covered {feature_data['coverage_pct']}%):")
            for action in feature_data["actions"]:
                print(f"    - {action['name']}: {action['status']} ({action['coverage_pct']}%)")
                print(f"      source matches: {len(action['source_matches'])}")
                print(f"      test matches: {len(action['test_matches'])}")
        else:
            print(f"  coverage_pct: {feature_data['coverage_pct']}")
        print()


def save_report_json(report: Dict[str, Dict], out_path: Path) -> None:
    try:
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"Wrote JSON report to: {out_path}")
    except Exception as exc:
        print(f"Failed to write JSON report to {out_path}: {exc}")


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    report = build_coverage_report(repo_root)
    print_report(report)
    out_path = repo_root / "coverage_report.json"
    save_report_json(report, out_path)


if __name__ == "__main__":
    main()
