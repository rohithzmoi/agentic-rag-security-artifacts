#!/usr/bin/env python3
"""
generate_tables.py - Reproducibility artifact for SoK: Authorization in Multi-Agent RAG Systems

This script reads the systematization data from CSV files and regenerates
the paper's Table 1 (Defense Family Guarantees) and Table 2 (Deployment Patterns).

Usage:
    python generate_tables.py

Outputs:
    - outputs/table1_defense_families.md
    - outputs/table2_deployment_patterns.md
    - outputs/summary_statistics.txt
"""

import pandas as pd
import os
from pathlib import Path

# Symbol mappings matching paper notation
SYMBOLS = {
    'Yes': '✓',
    'No': '✗',
    'Conditional': '±',
    'Yes/Conditional': '✓/±',
    'Conditional/Yes': '±/✓',
    'Strong': 'Strong',
    'Weak': 'Weak',
    'N/A': 'N/A',
    'High': 'High',
    'Medium': 'Med',
    'Low': 'Low'
}

def load_data():
    """Load CSV data files."""
    data_dir = Path(__file__).parent.parent / 'data'
    
    defense_families = pd.read_csv(data_dir / 'defense_families.csv').fillna('—')
    deployment_patterns = pd.read_csv(data_dir / 'deployment_patterns.csv').fillna('—')
    failure_modes = pd.read_csv(data_dir / 'failure_modes.csv').fillna('—')
    
    return defense_families, deployment_patterns, failure_modes

def get_symbol(value):
    """Get symbol for a value, handling NaN and missing values."""
    if pd.isna(value) or value == '—' or value == '':
        return '—'
    return SYMBOLS.get(str(value), str(value))

def generate_table1_markdown(df):
    """Generate Table 1: Defense Family Guarantees (matches paper Table 1)."""
    
    header = "| Defense Family | AFR | Auth | Deleg | Stale | Deploy | Notes |\n"
    separator = "|---|---|---|---|---|---|---|\n"
    
    rows = []
    for _, row in df.iterrows():
        afr = get_symbol(row['afr_support'])
        auth = get_symbol(row['auth_correctness'])
        deleg = get_symbol(row['delegation_correctness'])
        stale = get_symbol(row['staleness_risk'])
        deploy = get_symbol(row['deployment_complexity'])
        
        rows.append(f"| {row['defense_id']} {row['defense_family']} | {afr} | {auth} | {deleg} | {stale} | {deploy} | {row['notes']} |")
    
    return header + separator + "\n".join(rows)

def generate_table2_markdown(df):
    """Generate Table 2: Deployment Patterns (matches paper Table 2)."""
    
    header = "| Representative Pattern | AFR | Auth | Deleg | State Iso. | Reason |\n"
    separator = "|---|---|---|---|---|---|\n"
    
    rows = []
    for _, row in df.iterrows():
        afr = get_symbol(row['afr_support'])
        auth = get_symbol(row['auth_correctness'])
        deleg = get_symbol(row['delegation_correctness'])
        state_iso = get_symbol(row['state_isolation'])
        reason = str(row['reason'])[:80] if row['reason'] != '—' else '—'
        
        rows.append(f"| {row['representative_pattern']} | {afr} | {auth} | {deleg} | {state_iso} | {reason}... |")
    
    return header + separator + "\n".join(rows)

def compute_statistics(defense_df, pattern_df, failure_df):
    """Compute summary statistics supporting paper claims O1-O5."""
    
    stats = []
    stats.append("=" * 60)
    stats.append("SUMMARY STATISTICS - SoK Authorization in Multi-Agent RAG")
    stats.append("=" * 60)
    stats.append("")
    
    # O1: Post-hoc filtering does not satisfy AFR
    no_afr = defense_df[defense_df['afr_support'] == 'No']
    stats.append(f"O1: Defense families that CANNOT satisfy AFR: {len(no_afr)}")
    for _, row in no_afr.iterrows():
        stats.append(f"    - {row['defense_id']}: {row['defense_family']}")
    stats.append("")
    
    # O2: Conditional AFR (tag-based approaches)
    cond_afr = defense_df[defense_df['afr_support'] == 'Conditional']
    stats.append(f"O2: Defense families with CONDITIONAL AFR: {len(cond_afr)}")
    for _, row in cond_afr.iterrows():
        stats.append(f"    - {row['defense_id']}: {row['defense_family']} ({row['notes']})")
    stats.append("")
    
    # O3: Delegation correctness gaps
    no_deleg = defense_df[defense_df['delegation_correctness'] == 'N/A']
    stats.append(f"O3: Defense families with NO delegation correctness: {len(no_deleg)}")
    stats.append("")
    
    # O4: Patterns achieving full AFR
    full_afr_patterns = pattern_df[pattern_df['afr_support'] == 'Yes']
    stats.append(f"O4: Deployment patterns with FULL AFR support: {len(full_afr_patterns)}")
    for _, row in full_afr_patterns.iterrows():
        stats.append(f"    - {row['representative_pattern']}")
    stats.append("")
    
    # O5: Negative result - patterns with all three properties
    # Check for Yes in AFR, Auth, Deleg, and State Isolation
    stats.append("O5: NEGATIVE RESULT VERIFICATION")
    stats.append("    Checking for patterns with AFR + Delegation + State Isolation...")
    full_pattern = pattern_df[
        (pattern_df['afr_support'] == 'Yes') & 
        (pattern_df['auth_correctness'] == 'Yes') & 
        (pattern_df['delegation_correctness'].isin(['Yes', 'Conditional/Yes'])) &
        (pattern_df['state_isolation'] == 'Yes')
    ]
    if len(full_pattern) == 0:
        stats.append("    CONFIRMED: No pattern achieves all three properties simultaneously")
        stats.append("    (AFR PEP pattern achieves AFR+Auth but State Isolation remains Conditional)")
    else:
        stats.append(f"    Found {len(full_pattern)} pattern(s) - review paper claims")
    stats.append("")
    
    # Failure modes summary
    stats.append("FAILURE MODES CLASSIFIED:")
    for _, row in failure_df.iterrows():
        stats.append(f"    {row['mode_id']}: {row['failure_mode']}")
    stats.append(f"    Total failure modes: {len(failure_df)}")
    stats.append("")
    
    stats.append("=" * 60)
    stats.append("All statistics derived from systematization data.")
    stats.append("See paper Sections 6-8 for full analysis.")
    stats.append("=" * 60)
    
    return "\n".join(stats)

def main():
    """Main entry point."""
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / 'outputs'
    output_dir.mkdir(exist_ok=True)
    
    # Load data
    print("Loading systematization data...")
    defense_df, pattern_df, failure_df = load_data()
    
    # Generate Table 1
    print("Generating Table 1: Defense Family Guarantees...")
    table1 = generate_table1_markdown(defense_df)
    with open(output_dir / 'table1_defense_families.md', 'w') as f:
        f.write("# Table 1: Qualitative Guarantee Analysis\n\n")
        f.write("AFR = Authorization-First Retrieval, Auth = Authorization Correctness, ")
        f.write("Deleg = Delegation Correctness, Stale = Staleness Risk, Deploy = Deployment Complexity\n\n")
        f.write("Legend: ✓ = Yes, ✗ = No, ± = Conditional\n\n")
        f.write(table1)
    print(f"  -> Saved to {output_dir / 'table1_defense_families.md'}")
    
    # Generate Table 2
    print("Generating Table 2: Deployment Patterns...")
    table2 = generate_table2_markdown(pattern_df)
    with open(output_dir / 'table2_deployment_patterns.md', 'w') as f:
        f.write("# Table 2: Representative Deployment Patterns\n\n")
        f.write("State Iso. = Isolation of caches, rerankers, and adaptive components across users\n\n")
        f.write("Legend: ✓ = Can guarantee, ✗ = Cannot guarantee by construction, ± = Conditional\n\n")
        f.write(table2)
    print(f"  -> Saved to {output_dir / 'table2_deployment_patterns.md'}")
    
    # Compute statistics
    print("Computing summary statistics...")
    stats = compute_statistics(defense_df, pattern_df, failure_df)
    with open(output_dir / 'summary_statistics.txt', 'w') as f:
        f.write(stats)
    print(f"  -> Saved to {output_dir / 'summary_statistics.txt'}")
    
    # Print statistics to console
    print("\n" + stats)
    
    print("\nDone! All outputs saved to:", output_dir)

if __name__ == "__main__":
    main()
