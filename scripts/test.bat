@echo off

setlocal

copy /Y pyproject.toml.windows pyproject.toml

pytest -s

endlocal