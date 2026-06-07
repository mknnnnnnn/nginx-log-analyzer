# from pathlib import Path
# import json

# CONFIG = Path(__file__).resolve().parent / "config.json"

# if CONFIG.exists():
#     with open(CONFIG, "r", encoding="utf-8") as f:
#         config = json.load(f)
# else:
#     config = {}


# def save_storage() -> None:
#     with open(CONFIG, "w", encoding="utf-8") as f:
#         json.dump(config, f, ensure_ascii=False, indent=4)


# def input_set_path(path: Path) -> None:
#     config["Default input path"] = str(path)
#     save_storage()


# def input_load_path() -> Path | None:
#     path = config.get("Default input path")
#     return Path(path) if path else None


# def output_set_path(path: Path) -> None:
#     config["Default output path"] = str(path)
#     save_storage()


# def output_load_path() -> Path | None:
#     path = config.get("Default output path")
#     return Path(path) if path else None
