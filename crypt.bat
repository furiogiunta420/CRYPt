@echo off
color 5
cd files
setlocal EnableDelayedExpansion 
mode 38, 18 
title CRYPt

if exist "ii4o2.txt" (
    goto passii
) else (
    mode 120, 30
    pip install dotenv
    pip install cryptography 
    echo chck > ii4o2.txt  
    mode 38, 18
    goto passii 
)

:passii
if exist ".env" (
    powershell rm .env 
    goto passs
) else goto passs  

:passs 
cls
echo Please input your password...
echo.
set /p ala=
echo password=!ala! > .env 

:loop 
cls
echo Type 0 to decrypt
echo.
echo Type 2 to encrypt
echo.
echo Type 5 for help
echo.
echo Type 9 to exit 
echo.
set /p ola=
if /I "!ola!"=="0" goto dee 
if /I "!ola!"=="2" goto enn 
if /I "!ola!"=="5" goto helpp
if /I "!ola!"=="9" goto endi 
goto loop 

:helpp 
cls
mode 120, 30 
echo This is a step by step guide. Please follow it carefully...
echo When you launch the app for the first time you will be prompted with installation of needed libraries
echo Settings will be saved in ii4o2.txt file if you delete it you will be prompted with installation again
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo ENCRYPTION:
echo.
echo Step 1: Place your .txt file in files folder 
echo Step 2: Run the CRYPt.bat shortcut and input your password
echo Step 3: Type in #2 and then type in your file name w/o .txt extenstion
echo Step 4: Choose if you want to keep or delete the unencrypted file
echo Step 5: Send your encrypted file safely
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo DECRYPTION:
echo.
echo Step 1: Place your encrypted file in files folder 
echo Step 2: Run CRYPt.bat shortcut and input your password(IT MUST MATCH THE ONE THE FILE WAS ENCRYPTED WITH!!!)
echo Step 3: Type in #0 and then the name of the file w/o any extensions
echo Step 4: Choose if you want to keep or delete your encrypted file
echo Step 5: View your decrypted file with its contents in original form
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Press any key to go back
pause >nul 
mode 38, 18
goto loop 


:enn 
cls 
echo Please input your text file name 
echo Without the extenstion
echo.
set /p kaa=
python encrypt_secure.py !kaa!.txt  
timeout /t 1 >nul 
move !kaa!.txt.encrypted ..

rem powershell rm !kaa!.txt.encrypted 

pause

:quee

echo --------------------------------------
echo.
echo Do you want to keep the original file?
echo.
echo 0 YES
echo.
echo 9 NO 
echo.
set /p jjj=
if /I "!jjj!"=="0" goto loop 
if /I "!jjj!"=="9" (
    powershell rm !kaa!.txt 
    goto loop
) else goto loop 
goto quee 

:dee 
cls
echo Please input your file name 
echo Without the extenstion
echo.
set /p uii=
python decrypt_secure.py !uii!.txt.encrypted
timeout /t 1 >nul
move !uii!.txt ..
timeout /t 1 >nul
pause 

:quee2 
echo --------------------------------------
echo.
echo Do you want to keep the original file?
echo.
echo 0 YES 
echo.
echo 9 NO 
echo.
set /p kkk=
if /I "!kkk!"=="0" goto loop
if /I "!kkk!"=="9" (
    powershell rm !uii!.txt.encrypted 
    goto loop  
) else goto loop 
goto quee2 

:endi 
powershell rm .env 
exit 