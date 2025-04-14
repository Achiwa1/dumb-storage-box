@echo off
REM === Convert Python Script to Executable (.exe) ===
REM This batch file uses PyInstaller to package AchiwaLauncher.py into an executable.

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo PyInstaller is not installed. Installing it now...
    pip install pyinstaller
)

REM Set the name of the Python script and output folder
SET "SCRIPT_NAME=AchiwaLauncher.py"
SET "OUTPUT_DIR=dist"
SET "BUILD_DIR=build"

REM Remove old build directories if they exist
IF EXIST "%BUILD_DIR%" (
    echo Removing old build directory...
    rmdir /s /q "%BUILD_DIR%"
)
IF EXIST "%OUTPUT_DIR%" (
    echo Removing old dist directory...
    rmdir /s /q "%OUTPUT_DIR%"
)

REM Run PyInstaller to create the executable
echo Building executable from %SCRIPT_NAME%...
pyinstaller --onefile --noconsole "%SCRIPT_NAME%"

REM Check if the build was successful
IF EXIST "%OUTPUT_DIR%\AchiwaLauncher.exe" (
    echo Build successful! Keeping the executable in the current directory...
    move "%OUTPUT_DIR%\AchiwaLauncher.exe" . >nul

    REM Ensure required directories exist
    echo Ensuring required directories exist...
    mkdir games
    mkdir players
    mkdir skins
    mkdir thumbnails
    mkdir cloud_sync

    REM === Generate default and fun themes ===
    echo Generating themes in the skins directory...
    > skins\default.json echo {^
        "background": "#ffffff",^
        "foreground": "#000000",^
        "accent": "#0078d4",^
        "font": "Arial",^
        "font_size": 12^
    }

    > skins\dark_mode.json echo {^
        "background": "#1e1e1e",^
        "foreground": "#dcdcdc",^
        "accent": "#00bcd4",^
        "font": "Consolas",^
        "font_size": 12^
    }

    > skins\high_contrast.json echo {^
        "background": "#000000",^
        "foreground": "#ffffff",^
        "accent": "#ffcc00",^
        "font": "Verdana",^
        "font_size": 14^
    }

    > skins\retro_arcade.json echo {^
        "background": "#101010",^
        "foreground": "#00ff00",^
        "accent": "#ff0000",^
        "font": "Courier New",^
        "font_size": 16^
    }

    > skins\neon_lights.json echo {^
        "background": "#0d0d0d",^
        "foreground": "#e600ff",^
        "accent": "#00ffcc",^
        "font": "Lucida Console",^
        "font_size": 14^
    }

    > skins\solarized_light.json echo {^
        "background": "#fdf6e3",^
        "foreground": "#657b83",^
        "accent": "#268bd2",^
        "font": "Georgia",^
        "font_size": 12^
    }

    > skins\forest_adventure.json echo {^
        "background": "#013220",^
        "foreground": "#c8e6c9",^
        "accent": "#4caf50",^
        "font": "Trebuchet MS",^
        "font_size": 13^
    }

    > skins\candy_land.json echo {^
        "background": "#ffe6f0",^
        "foreground": "#ff1493",^
        "accent": "#ff69b4",^
        "font": "Comic Sans MS",^
        "font_size": 14^
    }

    > skins\sci_fi_futuristic.json echo {^
        "background": "#001f3f",^
        "foreground": "#7fdbff",^
        "accent": "#39cccc",^
        "font": "Orbitron",^
        "font_size": 14^
    }

    > skins\chaos_carnival.json echo {^
        "background": "#ff00ff",^
        "foreground": "#00ff00",^
        "accent": "#ffff00",^
        "font": "Papyrus",^
        "font_size": 20^
    }
    echo Themes generated successfully.

    REM === Scan for .zip files and extract them ===
    echo Scanning for .zip files to extract .swf and .exe files...
    for %%F in (*.zip) do (
        echo Extracting %%F...
        powershell -Command "Expand-Archive -Path '%%F' -DestinationPath '.' -Force"

        REM Move .swf files to the games directory
        for /r %%I in (*.swf) do (
            move "%%I" "games\" >nul
        )

        REM Move .exe files to the players directory, excluding the launcher executable
        for /r %%I in (*.exe) do (
            if /i not "%%~nxI"=="AchiwaLauncher.exe" (
                move "%%I" "players\" >nul
            )
        )
    )
    echo Extraction and organization complete.

    echo Build process complete.
) ELSE (
    echo Build failed. Please check for errors in the script or PyInstaller configuration.
)

pause