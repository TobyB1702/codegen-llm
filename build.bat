@echo off
setlocal

REM Nuitka standalone build — produces dist\app.dist\app.exe
REM Run from project root with the venv active: build.bat

python -m nuitka ^
    --standalone ^
    --assume-yes-for-downloads ^
    --include-package=src ^
    --include-package=langchain_core ^
    --include-package=langchain ^
    --include-package=langchain_anthropic ^
    --include-package=deepagents ^
    --include-data-files=data/top_rated_2000webseries.csv=data/top_rated_2000webseries.csv ^
    --output-dir=dist ^
    --output-filename=app ^
    src\app.py

echo.
echo Build complete. Run: dist\app.dist\app.exe
endlocal
