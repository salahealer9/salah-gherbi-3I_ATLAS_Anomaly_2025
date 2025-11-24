#!/usr/bin/env python3
"""
Quick script to show the exact formatting
"""

# This is how your magnitude parsing should look:
sample_code = '''
        # Simple, reliable magnitude parsing - second-to-last field is always magnitude
        parts = line.split()
        if len(parts) >= 2:
            potential_mag = parts[-2]
            if potential_mag.replace(".", "").isdigit():
                mag = float(potential_mag)
            else:
                mag = None
        else:
            mag = None
'''

print("Copy this exact code into your script:")
print(sample_code)
