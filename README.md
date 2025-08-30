# ts-visualizer

A tiny tool to ingest, summarize, plot, and export time series CSV files using a YAML config.

## Quick start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Adjust `config.yaml` to match your data source and columns.
3. Run a command:
   ```bash
   python -m tsvisualizer.cli ingest
   python -m tsvisualizer.cli summarize
   python -m tsvisualizer.cli plot
   python -m tsvisualizer.cli export
   ```

Outputs go to the `output/` directory.
