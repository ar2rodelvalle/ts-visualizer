import argparse
from pathlib import Path

import pandas as pd
import yaml
import matplotlib.pyplot as plt


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def ingest(cfg: dict) -> pd.DataFrame:
    source = Path(cfg["data"]["source"])
    pattern = cfg["data"]["pattern"]
    files = sorted(source.glob(pattern))
    dfs = []
    cols = cfg["columns"]
    group_cols = cols.get("grouping", [])
    for f in files:
        df = pd.read_csv(f)
        rename = {cols["time"]: "time", cols["value"]: "value"}
        for g in group_cols:
            rename.setdefault(g, g)
        df = df.rename(columns=rename)
        df["time"] = pd.to_datetime(df["time"])
        dfs.append(df[["time", "value"] + group_cols])
    return pd.concat(dfs, ignore_index=True)


def summarize(df: pd.DataFrame, group_cols: list) -> dict:
    summary = {
        "rows": len(df),
        "time_start": df["time"].min(),
        "time_end": df["time"].max(),
        "groups": {c: df[c].nunique() for c in group_cols},
    }
    return summary


def plot(df: pd.DataFrame, group_cols: list, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, group in df.groupby(group_cols):
        label = "_".join(name) if isinstance(name, tuple) else name
        ax = group.sort_values("time").plot(x="time", y="value", title=label)
        fig = ax.get_figure()
        fig.tight_layout()
        fig.savefig(out_dir / f"{label}.png")
        plt.close(fig)


def export(df: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "combined.csv", index=False)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["ingest", "summarize", "plot", "export"])
    p.add_argument("--config", default="config.yaml")
    args = p.parse_args()

    cfg = load_config(args.config)
    df = ingest(cfg)
    group_cols = cfg["columns"].get("grouping", [])
    out_dir = Path(cfg["output"]["dir"])

    if args.command == "ingest":
        print(df.head())
    elif args.command == "summarize":
        print(summarize(df, group_cols))
    elif args.command == "plot":
        plot(df, group_cols, out_dir / "plots")
    elif args.command == "export":
        export(df, out_dir)


if __name__ == "__main__":
    main()
