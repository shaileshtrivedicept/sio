# Studio Review Dashboard

Interactive Streamlit dashboard for analyzing and visualizing studio review performance data.

## Features
- **Key Performance Indicators (KPIs)**: Tracking total studios, panels, response counts, average scores, and panel spread.
- **Studio Trajectory**: Visualizing performance over semesters with chronological sorting and total score overlays.
- **Construct Contribution Heatmap**: Analyzing the distribution of score contributions across various constructs.
- **Final Score Distribution**: Box plots of scores categorized by Construct ID, with optional Panel ID faceting.
- **Performance Rankings**: Top and Bottom 10 studios for selected semesters.
- **Data Export**: Downloadable CSV files for filtered raw data and calculated metrics.

## Getting Started

### Prerequisites
- Python 3.8 or higher
-
Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  lock                        Generate a lock file.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  inspect                     Inspect the python environment.
  list                        List installed packages.
  show                        Show information about installed packages.
  check                       Verify installed packages have compatible dependencies.
  config                      Manage local and global configuration.
  search                      Search PyPI for packages.
  cache                       Inspect and manage pip's wheel cache.
  index                       Inspect information available from package indexes.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion.
  debug                       Show information useful for debugging.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --debug                     Let unhandled exceptions propagate outside the
                              main subroutine, instead of logging them to
                              stderr.
  --isolated                  Run pip in an isolated mode, ignoring
                              environment variables and user configuration.
  --require-virtualenv        Allow pip to only run in a virtual environment;
                              exit with an error otherwise.
  --python <python>           Run pip with the specified Python interpreter.
  -v, --verbose               Give more output. Option is additive, and can be
                              used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output. Option is additive, and can be
                              used up to 3 times (corresponding to WARNING,
                              ERROR, and CRITICAL logging levels).
  --log <path>                Path to a verbose appending log.
  --no-input                  Disable prompting for input.
  --keyring-provider <keyring_provider>
                              Enable the credential lookup via the keyring
                              library if user input is allowed. Specify which
                              mechanism to use [auto, disabled, import,
                              subprocess]. (default: auto)
  --proxy <proxy>             Specify a proxy in the form
                              scheme://[user:passwd@]proxy.server:port.
  --retries <retries>         Maximum attempts to establish a new HTTP
                              connection. (default: 5)
  --timeout <sec>             Set the socket timeout (default 15 seconds).
  --exists-action <action>    Default action when a path already exists:
                              (s)witch, (i)gnore, (w)ipe, (b)ackup, (a)bort.
  --trusted-host <hostname>   Mark this host or host:port pair as trusted,
                              even though it does not have valid or any HTTPS.
  --cert <path>               Path to PEM-encoded CA certificate bundle. If
                              provided, overrides the default. See 'SSL
                              Certificate Verification' in pip documentation
                              for more information.
  --client-cert <path>        Path to SSL client certificate, a single file
                              containing the private key and the certificate
                              in PEM format.
  --cache-dir <dir>           Store the cache data in <dir>.
  --no-cache-dir              Disable the cache.
  --disable-pip-version-check
                              Don't periodically check PyPI to determine
                              whether a new version of pip is available for
                              download. Implied with --no-index.
  --no-color                  Suppress colored output.
  --use-feature <feature>     Enable new functionality, that may be backward
                              incompatible.
  --use-deprecated <feature>  Enable deprecated functionality, that will be
                              removed in the future.
  --resume-retries <resume_retries>
                              Maximum attempts to resume or restart an
                              incomplete download. (default: 5)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
Run the Streamlit application from the root directory:
```bash
streamlit run app.py
```

## Data Management
The dashboard reads data from: `data/BoR_Rating_Data.xlsx`.

To update the data:
1. Replace the file in the `data/` directory.
2. Ensure the sheet name is 'Normalized Score' or update the loading logic in `src/io.py`.
3. Column names should remain consistent (AY, Semester, Studio_Code, Panel_ID, Final_Score, etc.).

## Project Structure
- `app.py`: Main Streamlit application entry point.
- `data/`: Directory for the Excel data source.
- `src/io.py`: Data ingestion and cleaning logic.
- `src/metrics.py`: Business logic for aggregating scores and computing shares.
- `requirements.txt`: Python package dependencies.
