# Use the official Windows Server Core image as the base image
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Set timezone environment variable (optional)
ENV TZ=Asia/Kolkata

# Set the working directory inside the container
WORKDIR /app

# Copy your bot.py (Python bot file) and any other necessary files into the container
COPY bot.py /app
COPY requirements.txt /app
COPY N_m3u8DL-CLI_v3.0.2.exe /app
COPY mp4decrypt.exe /app
COPY mkvmerge.exe /app
COPY sync_time.bat /app

# Install Python and dependencies
RUN powershell -Command \
    Set-ExecutionPolicy RemoteSigned -Scope Process -Force; \
    Invoke-WebRequest https://www.python.org/ftp/python/3.10.8/python-3.10.8.exe -OutFile python-installer.exe; \
    Start-Process -Wait -FilePath python-installer.exe /quiet InstallAllUsers=1 PrependPath=1; \
    Remove-Item -Force python-installer.exe; \
    python -m pip install --upgrade pip; \
    pip install -r requirements.txt

# Run the time sync script to sync the time with NTP
RUN sync_time.bat

# Set the default command to run your bot.py script
CMD ["python", "bot.py"]
