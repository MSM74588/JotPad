# Name of the installer
OutFile "JotPadInstaller.exe"

# The default installation directory
InstallDir "$PROGRAMFILES\JotPad"

# Define the icon for the installer
Icon "icon.ico"

# The directory where the installer will extract the files
SetOutPath "$INSTDIR"

# Request application privileges for Windows Vista
RequestExecutionLevel admin

# Define the files to be included in the installer
Section "MainSection" SEC01
  # Main executable
  SetOutPath "$INSTDIR"
  File "dist\JotPad\JotPad.exe"

  # Additional files
  File /r "dist\JotPad\*"
  File /r "colorschemes\*"
  File "icon.ico"

  # Create a shortcut in the start menu
  CreateShortCut "$SMPROGRAMS\JotPad.lnk" "$INSTDIR\JotPad.exe"
  # Create a shortcut on the desktop
  CreateShortCut "$DESKTOP\JotPad.lnk" "$INSTDIR\JotPad.exe"
SectionEnd

# Uninstaller section
Section "Uninstall"
  Delete "$INSTDIR\JotPad.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\colorschemes\*.*"
  RMDir /r "$INSTDIR\colorschemes"
  RMDir "$INSTDIR"

  Delete "$SMPROGRAMS\JotPad.lnk"
  Delete "$DESKTOP\JotPad.lnk"
SectionEnd
