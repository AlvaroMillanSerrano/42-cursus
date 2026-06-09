if __name__ == "__main__":
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    try:
        print("Accessing Storage Vault: ancient_fragment.txt")
        ancient_fd = open("ancient_fragment.txt", "r")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Connection established...\n")
        print("RECOVERED DATA:")
        content = ancient_fd.read()
        print(content)
        ancient_fd.close()
        print("\nData recovery complete. Storage unit disconnected.")
