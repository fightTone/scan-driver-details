import subprocess
import pandas as pd
import wmi
import sys
import os

# Set display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Run driverquery command and capture its output
driverquery_output = subprocess.check_output(["driverquery"], text=True)

# Process driverquery output to get basic driver details
basic_details = []
for line in driverquery_output.split('\n'):
    fields = line.strip().split()
    if len(fields) >= 4:
        basic_details.append({
            'Module Name': fields[0],
            'Display Name': fields[1],
            'Driver Type': fields[2],
            'Link Date': " ".join(fields[3:])
        })

# Connect to the WMI service
c = wmi.WMI()

# Get additional details using WMI
additional_details = []
for driver in c.Win32_SystemDriver():
    # Get the file path of the driver
    file_path = driver.PathName
    # Get the signature information
    try:
        signature = subprocess.check_output(["powershell", "Get-AuthenticodeSignature", "-FilePath", file_path], text=True)
        signature_exists = "True"
    except subprocess.CalledProcessError:
        signature = "No signature"
        signature_exists = "False"

    # Append additional details to the list
    additional_details.append({
        'Module Name': driver.Name,
        'State': driver.State,
        'File Path': file_path,
        'Description': driver.Description,
        'ServiceType': driver.ServiceType,
        'Started': driver.Started,
        'StartMode': driver.StartMode,
        'StartName': driver.StartName,
        'Caption': driver.Caption,
        'InstallDate': driver.InstallDate,
        'Status': driver.Status,
        'ErrorControl': driver.ErrorControl,
        'TagId': driver.TagId,
        'AcceptPause': driver.AcceptPause,
        'AcceptStop': driver.AcceptStop,
        'SystemCreationClassName': driver.SystemCreationClassName,
        'SystemName': driver.SystemName,
        'ServiceSpecificExitCode': driver.ServiceSpecificExitCode,
        'ExitCode': driver.ExitCode,
        'DesktopInteract': driver.DesktopInteract,
        'SystemCreationClassName': driver.SystemCreationClassName,
        'SystemName': driver.SystemName,
        'Signature': signature,
        'Signature Exists': signature_exists
    })

# Merge basic and additional details
merged_details = []
for basic_detail in basic_details:
    for additional_detail in additional_details:
        if basic_detail['Module Name'] == additional_detail['Module Name']:
            merged_detail = basic_detail.copy()
            merged_detail.update(additional_detail)
            merged_details.append(merged_detail)
            break

# Create DataFrame
df = pd.DataFrame(merged_details)

# Display entire DataFrame
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
    print(df)
