# Sauce Demo UI Tests (Playwright + Python)

UI test suite for https://www.saucedemo.com using Playwright for Python, pytest, pytest-playwright and pytest-xdist. Ready to run on Azure Pipelines.

## Setup
```
python -m venv .venv
.venv\Scripts\activate            # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run locally
| Goal | Command |
|---|---|
| Everything (parallel, with reports) | `.\run_tests.ps1` (Windows) or `make test` |
| Smoke subset | `pytest -m smoke` |
| Regression subset | `pytest -m regression` |
| Single test | `pytest tests/test_cart.py::test_remove_item_updates_buttons_and_badge` |
| Another browser | `pytest --browser firefox` (or `webkit`) |
| Watch the browser | `pytest --headed -n 0` |
| Other credentials | `pytest --sauce-user X --sauce-password Y` or env `SAUCE_USER` / `SAUCE_PASSWORD` |

Reports go to `reports/` (JUnit XML + HTML). Traces, screenshots and videos for **failed tests only** go to `test-results/`.
Open a trace: `playwright show-trace test-results/<test-folder>/trace.zip`

## Project layout
```
pages/    page objects (one class per page, all locators live here)
tests/    test files: login, sorting, checkout e2e, checkout validation, cart
conftest.py   fixtures: page objects, credentials, login-once storage state
pytest.ini    base URL, reporting, failure artifacts, markers
```

## Design decisions
- **Page Object Model**: locators and page actions live in `pages/`; tests contain only scenario steps and assertions. Page objects are exposed as fixtures in `conftest.py`.
- **Login once**: a session-scoped fixture logs in and saves storage state; every test reuses it via `browser_context_args`. Tests marked `@pytest.mark.anonymous` (login tests) start logged out. Under xdist this runs once per worker. I override `browser_context_args` instead of creating my own context so pytest-playwright's built-in trace/screenshot/video-on-failure still works.
- **Locators**: test-id locators; `data-test` is configured as the test-id attribute because Sauce Demo does not use `data-testid`.
- **No sleeps**: only auto-waiting and web-first `expect(...)` assertions.
- **Sorting** compares the real displayed order against an expected list computed in Python, not just the dropdown value.
- **Money maths** uses `Decimal` to avoid float rounding errors.
- **Config**: base URL, reporting and artifacts in `pytest.ini`; browser via `--browser`; credentials via CLI options or env vars (defaults are the public demo credentials).
- **Markers**: `smoke`, `regression`, `anonymous`.

## Pipeline (`azure-pipelines.yml`)
1. Triggers on every push and pull request to `main`.
2. Agent pool is parameterised: `poolType` = `hosted` (Microsoft-hosted `ubuntu-latest`) or `selfhosted` (pool name in `selfHostedPoolName`).
3. A matrix runs Chromium, Firefox and WebKit as separate legs.
4. `UsePythonVersion@0` selects Python 3.11.
5. Install dependencies from the pinned `requirements.txt`.
6. `playwright install --with-deps <browser>` installs the browser and OS libraries.
7. Run pytest in parallel (xdist), writing JUnit XML and an HTML report to `reports/`.
8. `PublishTestResults@2` publishes the JUnit results (runs even if tests fail).
9. Publish `reports/` as a pipeline artifact.
10. On failure only, publish `test-results/` (traces, screenshots, videos).

## Sample reports
`sample-reports/` contains the JUnit XML and HTML report from one local run.

## Docker (bonus)
```
docker build -t saucedemo-tests .
docker run --rm -v "$PWD/reports:/app/reports" saucedemo-tests
```

## Assumptions
- The demo site is public; its credentials are not secrets.
- Site data resets on each page load, so tests are independent.

## With more time
Allure reporting, test data factories, lint/format step in CI, retry policy for flaky tests, visual checks, more negative scenarios.

## AI usage
I used an AI assistant to plan the structure, draft the pytest and pipeline code, and explain concepts. I ran, reviewed and adjusted the tests myself and can explain every line.
