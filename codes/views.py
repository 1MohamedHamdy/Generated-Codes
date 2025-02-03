from django.shortcuts import render, redirect
from django.contrib import messages
import fcntl
import re
from .forms import CodeForm

CODES_FILE = "codes.txt"

def home(request):
    return render(request, "codes/index.html")

def add_code(request):
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            input_codes = form.cleaned_data["codes"]
            new_codes = [code.strip().upper() for code in re.split(r'\s+', input_codes) if code.strip()]
            valid_codes = []
            duplicates = []
            invalid = []
            
            for code in new_codes:
                if len(code) != 8 or not code.isalnum():
                    invalid.append(code)
                else:
                    valid_codes.append(code)
            
            if valid_codes:
                with open(CODES_FILE, "a+") as file:
                    fcntl.flock(file, fcntl.LOCK_EX)
                    file.seek(0)
                    existing_codes = [c.strip() for c in file.readlines()]
                    added_codes = []
                    
                    for code in valid_codes:
                        if code not in existing_codes:
                            file.write(f"{code}\n")
                            added_codes.append(code)
                        else:
                            duplicates.append(code)
                    
                    fcntl.flock(file, fcntl.LOCK_UN)
                    
                    if added_codes:
                        messages.success(request, f"Added {len(added_codes)} codes: {', '.join(added_codes)}")
                    if duplicates:
                        messages.warning(request, f"Duplicate codes skipped: {', '.join(duplicates)}")
                    if invalid:
                        messages.error(request, f"Invalid codes (must be 8 alphanumeric characters): {', '.join(invalid)}")
            
            return redirect("view_codes")
    else:
        form = CodeForm()
    
    return render(request, "codes/add_code.html", {"form": form})

def view_codes(request):
    try:
        with open(CODES_FILE, "r") as file:
            codes = [c.strip() for c in file.readlines() if c.strip()]
    except FileNotFoundError:
        codes = []
    
    return render(request, "codes/codes.html", {
        "codes": codes,
        "total_codes": len(codes)
    })

def remove_code(request, code):
    with open(CODES_FILE, "r+") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        codes = [c.strip() for c in file.readlines()]
        if code in codes:
            codes.remove(code)
            file.seek(0)
            file.truncate()
            file.write("\n".join(codes))
            messages.success(request, f"Code '{code}' removed successfully!")
        else:
            messages.error(request, f"Code '{code}' not found!")
        fcntl.flock(file, fcntl.LOCK_UN)
    return redirect("view_codes")