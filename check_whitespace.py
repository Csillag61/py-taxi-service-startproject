"""
Whitespace and Indentation Checker for Django Project
"""

import os
import re

def check_file_whitespace(filepath):
    """Check a file for whitespace and indentation issues"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Check for trailing whitespace
            if line.rstrip() != line.rstrip('\n'):
                issues.append(f"Line {i}: Trailing whitespace")
            
            # Check for tabs (should use spaces)
            if '\t' in line:
                issues.append(f"Line {i}: Contains tabs (should use spaces)")
            
            # Check for inconsistent indentation (Python should use 4 spaces)
            if line.startswith(' ') and not line.startswith('    '):
                # Count leading spaces
                leading_spaces = len(line) - len(line.lstrip(' '))
                if leading_spaces % 4 != 0:
                    issues.append(f"Line {i}: Inconsistent indentation ({leading_spaces} spaces)")
        
        # Check if file ends with newline
        if lines and not lines[-1].endswith('\n'):
            issues.append("File doesn't end with newline")
            
    except Exception as e:
        issues.append(f"Error reading file: {e}")
    
    return issues

def check_python_files():
    """Check all Python files in the project"""
    python_files = [
        'taxi/models.py',
        'taxi/admin.py', 
        'taxi/views.py',
        'taxi/apps.py',
        'taxi_service/settings.py',
        'taxi_service/urls.py',
        'manage.py'
    ]
    
    print("🔍 CHECKING PYTHON FILES FOR WHITESPACE/INDENTATION ISSUES\n")
    
    all_clean = True
    
    for file_path in python_files:
        if os.path.exists(file_path):
            print(f"📋 Checking {file_path}...")
            issues = check_file_whitespace(file_path)
            
            if issues:
                all_clean = False
                print(f"  ❌ Found {len(issues)} issue(s):")
                for issue in issues:
                    print(f"    - {issue}")
            else:
                print(f"  ✅ Clean - no whitespace issues")
        else:
            print(f"  ⚠️ File not found: {file_path}")
        print()
    
    return all_clean

def check_markdown_files():
    """Check markdown files for formatting"""
    md_files = ['README.md', 'checklist.md']
    
    print("📝 CHECKING MARKDOWN FILES\n")
    
    for file_path in md_files:
        if os.path.exists(file_path):
            print(f"📋 Checking {file_path}...")
            issues = check_file_whitespace(file_path)
            
            if issues:
                print(f"  ❌ Found {len(issues)} issue(s):")
                for issue in issues:
                    print(f"    - {issue}")
            else:
                print(f"  ✅ Clean - no whitespace issues")
        else:
            print(f"  ⚠️ File not found: {file_path}")
        print()

def check_specific_python_standards():
    """Check for specific Python coding standards"""
    print("🐍 CHECKING PYTHON CODING STANDARDS\n")
    
    files_to_check = ['taxi/models.py', 'taxi/admin.py']
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"📋 Checking {file_path} for PEP 8 compliance...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            issues = []
            
            # Check for proper class spacing (2 blank lines before class)
            for i, line in enumerate(lines):
                if line.startswith('class ') and i > 0:
                    # Count blank lines before class
                    blank_count = 0
                    j = i - 1
                    while j >= 0 and lines[j].strip() == '':
                        blank_count += 1
                        j -= 1
                    
                    if j >= 0 and blank_count < 2:
                        issues.append(f"Line {i+1}: Class should have 2 blank lines before it")
            
            # Check for proper method spacing (1 blank line before method)
            for i, line in enumerate(lines):
                if re.match(r'    def ', line) and i > 0:
                    if lines[i-1].strip() != '':
                        issues.append(f"Line {i+1}: Method should have 1 blank line before it")
            
            # Check line length (should be <= 79 characters)
            for i, line in enumerate(lines):
                if len(line) > 79:
                    issues.append(f"Line {i+1}: Line too long ({len(line)} > 79 characters)")
            
            if issues:
                print(f"  ❌ Found {len(issues)} PEP 8 issue(s):")
                for issue in issues:
                    print(f"    - {issue}")
            else:
                print(f"  ✅ PEP 8 compliant")
        print()

def main():
    """Run all checks"""
    print("=" * 60)
    print("🧹 DJANGO PROJECT WHITESPACE & INDENTATION CHECKER")
    print("=" * 60)
    print()
    
    # Change to project directory
    os.chdir('f:/aaPYTHON/DJANGO/py-taxi-service-startproject')
    
    python_clean = check_python_files()
    check_markdown_files()
    check_specific_python_standards()
    
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if python_clean:
        print("✅ All Python files have clean whitespace and indentation!")
    else:
        print("❌ Some Python files have whitespace/indentation issues")
    
    print("\n🎯 RECOMMENDATIONS:")
    print("- Use 4 spaces for indentation (not tabs)")
    print("- Remove trailing whitespace")
    print("- Ensure files end with a newline")
    print("- Follow PEP 8 guidelines")
    print("- Use an IDE with Python formatting (like VS Code with Python extension)")

if __name__ == "__main__":
    main()
