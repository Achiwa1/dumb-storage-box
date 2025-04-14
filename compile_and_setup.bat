@echo off
setlocal enabledelayedexpansion

echo [AchiwaOS Installer] Launching setup...
echo -------------------------------------------------- > install_log.txt
echo Install started: %DATE% %TIME% >> install_log.txt

:: Compile launcher
echo Compiling launcher... >> install_log.txt
python -m PyInstaller --onefile --noconsole achiwa_ai_launcher.py >> install_log.txt 2>&1

:: Move exe and cleanup
if exist dist\achiwa_ai_launcher.exe move /Y dist\achiwa_ai_launcher.exe . >> install_log.txt 2>&1
if not exist achiwa_ai_launcher.exe echo [ERROR] Launcher EXE not found after build! >> install_log.txt
rd /s /q build >> install_log.txt 2>&1
rd /s /q dist >> install_log.txt 2>&1
del achiwa_ai_launcher.spec >> install_log.txt 2>&1

:: Create games folder if not exist
if not exist games (
    mkdir games
    echo [INFO] Created 'games' folder. >> install_log.txt
)

:: Extract flash players
echo Extracting Flash Players... >> install_log.txt
for %%F in (players\*.zip) do (
    echo - Extracting %%~nxF >> install_log.txt
    powershell.exe -Command "Expand-Archive -Force '%%F' 'players\\%%~nF'" >> install_log.txt 2>&1
)

:: Temp extraction folder
set tempdir=temp_extract
if exist %tempdir% rd /s /q %tempdir%

:: Process all zips
for %%Z in (*.zip) do (
    echo - Extracting archive %%~nxZ... >> install_log.txt
    powershell.exe -Command "Expand-Archive -Force '%%Z' '%tempdir%\\%%~nZ'" >> install_log.txt 2>&1

    echo - Analyzing %%~nZ for SWFs in root AND subfolders... >> install_log.txt

    powershell.exe -NoProfile -Command ^
        "$base = Resolve-Path '%tempdir%\\%%~nZ';" ^
        "$rootSWFs = Get-ChildItem $base -Filter *.swf;" ^
        "if ($rootSWFs.Count -ge 3) {" ^
            "Add-Content 'install_log.txt' ('-- Copying root files from ' + $base);" ^
            "Copy-Item ($base.Path + '\\*') -Destination 'games' -Recurse -Force;" ^
        "} else {" ^
            "Add-Content 'install_log.txt' ('-- Root skipped (SWFs: ' + $rootSWFs.Count + ')');" ^
        "};" ^
        "$folders = Get-ChildItem $base -Recurse -Directory;" ^
        "foreach ($folder in $folders) {" ^
            "$swfs = Get-ChildItem $folder.FullName -Recurse -Include *.swf;" ^
            "if ($swfs.Count -ge 3) {" ^
                "Add-Content 'install_log.txt' ('-- Copying from: ' + $folder.FullName);" ^
                "Copy-Item $folder.FullName\* -Destination 'games' -Recurse -Force;" ^
            "} else {" ^
                "Add-Content 'install_log.txt' ('-- Skipped: ' + $folder.FullName + ' (SWFs found: ' + $swfs.Count + ')');" ^
            "}" ^
        "}" >> install_log.txt 2>&1

    echo - Cleaning up %%~nxZ and extracted files... >> install_log.txt
    del "%%Z" >> install_log.txt 2>&1
    rd /s /q "%tempdir%\\%%~nZ"
)

rd /s /q %tempdir%

echo Install complete: %DATE% %TIME% >> install_log.txt
echo [AchiwaOS Installer] Done. Press any key to close.
pause
del achiwa_ai_launcher.py >nul 2>&1
del "%~f0"
