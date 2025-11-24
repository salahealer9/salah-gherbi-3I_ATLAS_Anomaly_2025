#!/usr/bin/env python3
import re
import pandas as pd

MPC_FILE = "I3.txt"

print("🔍 DEBUGGING MAGNITUDE PARSING FOR NOVEMBER DATA")
print("=" * 60)

rows = []
problem_lines = []

with open(MPC_FILE) as f:
    for line_num, line in enumerate(f, 1):
        if not line.startswith("0003I"):
            continue
        
        # Check if it's November data
        if "2025 11" in line:
            print(f"\n=== Line {line_num}: {line.strip()}")
            
            # Your original parsing logic
            m = re.search(r"2025\s(\d{2})\s(\d{2}\.\d+)", line)
            if m:
                month = int(m.group(1))
                dayf = float(m.group(2))
                print(f"  Date parsed: 2025-{month:02d}-{int(dayf):02d}")
            
            # First regex attempt
            magm = re.search(r"(\d{1,2}\.\d{1,2})\s*([A-Za-z]?)", line)
            if magm:
                print(f"  First regex match: '{magm.group(1)}' at position {magm.start()}")
                mag1 = float(magm.group(1))
            else:
                print("  First regex: No match")
                mag1 = None
            
            # Second regex attempt  
            magm2 = re.search(r"\s(\d{1,2}\.\d{1,2})\s", line)
            if magm2:
                print(f"  Second regex match: '{magm2.group(1)}' at position {magm2.start()}")
                mag2 = float(magm2.group(1))
            else:
                print("  Second regex: No match")
                mag2 = None
            
            # Let's also check what's at position 33:38 (your original approach)
            mag_str_orig = line[33:38].strip()
            print(f"  Original position [33:38]: '{mag_str_orig}'")
            
            # Use whichever magnitude was found
            if magm:
                mag = mag1
            elif magm2:
                mag = mag2
            else:
                mag = None
                
            print(f"  FINAL MAGNITUDE: {mag}")
            
            # Check if this is one of the problematic low magnitudes
            if mag and mag < 5:
                problem_lines.append((line_num, line.strip(), mag))
                print(f"  ⚠️  PROBLEM: Unrealistically bright magnitude {mag}")
            
            day_int = int(dayf)
            frac_day = dayf - day_int
            date = pd.Timestamp(2025, month, day_int, tz="UTC") + pd.to_timedelta(frac_day * 24, unit="h")
            rows.append({"date": date, "mag": mag})

print(f"\n=== SUMMARY ===")
print(f"Total November observations parsed: {len(rows)}")
print(f"Problematic lines (mag < 5): {len(problem_lines)}")

if problem_lines:
    print(f"\n⚠️  PROBLEMATIC LINES FOUND:")
    for line_num, line, mag in problem_lines:
        print(f"  Line {line_num}: mag={mag} -> {line}")

# Create dataframe and check daily averages
if rows:
    df = pd.DataFrame(rows)
    df["day"] = df["date"].dt.floor("D")
    df_with_mag = df[df['mag'].notna()].copy()
    df_daily = df_with_mag.groupby("day")["mag"].mean().reset_index()
    
    print(f"\n=== DAILY AVERAGES FOR NOVEMBER ===")
    for idx, row in df_daily.iterrows():
        print(f"  {row['day'].date()}: {row['mag']:.2f}")
