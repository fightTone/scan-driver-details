import wmi

# Connect to the WMI service
c = wmi.WMI()

# Get the first Win32_SystemDriver instance
driver = next(iter(c.Win32_SystemDriver()), None)

# Print all available attributes
if driver:
    for attribute in dir(driver):
        if not attribute.startswith('_'):
            try:
                value = getattr(driver, attribute)
                print(f"{attribute}: {value}")
            except Exception as e:
                print(f"Error accessing attribute {attribute}: {str(e)}")
