if __name__ == "__main__":
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
    try:
        with open("lost_archive.txt", "r") as lost_fd:
            print(
                "\nROUTINE ACCESS: Attempting "
                "access to 'lost_archive.txt'..."
            )
            print(lost_fd.read())
    except Exception as e:
        print("\nCRISIS ALERT: Attempting access to 'lost_archive.txt'...")
        if isinstance(e, FileNotFoundError):
            print("RESPONSE: Archive not found in storage matrix")
        elif isinstance(e, PermissionError):
            print("RESPONSE: Security protocols deny access")
        else:
            print(f"RESPONSE: {e}")
        print("STATUS: Crisis handled, security maintained")
    else:
        print("SUCCESS: Archive recovered - ``Knowledge preserved for humanity''")
        print("STATUS: Normal operations resumed")
    try:
        with open("classified_vault.txt", "r") as class_fd:
            print(
                "\nROUTINE ACCESS: Attempting access "
                "to 'classified_archive.txt'..."
            )
            print(class_fd.read())
    except Exception as e:
        print("\nCRISIS ALERT: Attempting access to 'classified_vault.txt'...")
        if isinstance(e, FileNotFoundError):
            print("RESPONSE: Archive not found in storage matrix")
        elif isinstance(e, PermissionError):
            print("RESPONSE: Security protocols deny access")
        else:
            print(f"RESPONSE: {e}")
        print("STATUS: Crisis handled, security maintained")
    else:
        print("SUCCESS: Archive recovered - ``Knowledge preserved for humanity''")
        print("STATUS: Normal operations resumed")
    try:
        with open("standard_archive.txt", "r"):
            print(
                "\nROUTINE ACCESS: Attempting "
                "access to 'standard_archive.txt'..."
            )
    except Exception as e:
        print("\nCRISIS ALERT: Attempting access to 'standard_archive.txt'...")
        if isinstance(e, FileNotFoundError):
            print("RESPONSE: Archive not found in storage matrix")
        elif isinstance(e, PermissionError):
            print("RESPONSE: Security protocols deny access")
        else:
            print(f"RESPONSE: {e}")
    else:
        print("SUCCESS: Archive recovered - ``Knowledge preserved for humanity''")
        print("STATUS: Normal operations resumed")
    print("\nAll crisis scenarios handled successfully. Archives secure.")
