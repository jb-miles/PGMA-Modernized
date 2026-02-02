import os

# Define the root directory for plugins
PLUGINS_DIR = "/Users/jbmiles/Library/Application Support/Plex Media Server/Plug-ins"

# The specific code to inject
INJECTION_CODE = "    log('UTILS :: IAFD Lookup Disabled to prevent 403 Errors.')\n    return\n"

# The target function definition to look for
TARGET_DEF = "def getFilmOnIAFD(AGENTDICT, FILMDICT):"

def patch_utils_file(filepath):
    """
    Patches a single utils.py file to disable getFilmOnIAFD.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        new_lines = []
        modified = False
        already_patched = False

        for line in lines:
            new_lines.append(line)
            
            # Check if we just added the function definition
            if TARGET_DEF in line:
                # Look ahead to see if it's already patched
                # (This is a simple check, looking at the next non-empty line would be more robust but this suffices for exact matches)
                pass 
            
            if TARGET_DEF in line:
                # Check if the next lines already contain the fix (to avoid double patching)
                # We'll handle this by setting a flag if we modify, but we should check context first.
                # Actually, simpler: just insert. If it duplicates, it's messy but valid python (unreachable code).
                # But let's be cleaner.
                pass

        # Let's try a rewrite approach
        final_lines = []
        for i, line in enumerate(lines):
            final_lines.append(line)
            if TARGET_DEF in line:
                # Check next line
                if i + 1 < len(lines) and "IAFD Lookup Disabled" in lines[i+1]:
                    print("Skipping {}: Already patched.".format(os.path.basename(os.path.dirname(os.path.dirname(filepath)))))
                    already_patched = True
                    break
                
                # Insert the code
                final_lines.append(INJECTION_CODE)
                modified = True
        
        if already_patched:
            return

        if modified:
            with open(filepath, 'w') as f:
                f.writelines(final_lines)
            print("Patched: {}".format(os.path.basename(os.path.dirname(os.path.dirname(filepath)))))
        else:
            # If we didn't find the target def, log it
            print("Target function not found in: {}".format(os.path.basename(os.path.dirname(os.path.dirname(filepath)))))

    except Exception as e:
        print("Error patching {}: {}".format(filepath, e))

def main():
    print("Starting mass patch of utils.py...")
    count = 0
    for root, dirs, files in os.walk(PLUGINS_DIR):
        for file in files:
            if file == "utils.py":
                # We only want the main utils.py in Code/, not in Libraries/
                if "/Contents/Code" in root:
                    patch_utils_file(os.path.join(root, file))
                    count += 1
    print("Processed {} files.".format(count))

if __name__ == "__main__":
    main()
