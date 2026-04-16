'''
AUTHOR: Ammar Hatiya
DATE: 2025/12/10
DESCRIPTION: AD Hygiene Auditor
'''
#!/usr/bin/env python3
import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta
import argparse
import os

def main():
    parser_obj = argparse.ArgumentParser()
    parser_obj.add_argument('--input', required=True)
    parser_obj.add_argument('--days-stale', type=int, default=90)
    parser_obj.add_argument('--output-dir', default='out')
    parser_obj.add_argument('--dry-run', action='store_true')
    args = parser_obj.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.input, parse_dates=['lastLogonTimestamp'])
    cutoff = datetime.now() - timedelta(days=args.days_stale)

    df['stale'] = df['lastLogonTimestamp'] < cutoff
    df['severity'] = 0

    # Stale (i.e. past the threshold for considering account 'expired') but still enabled
    df.loc[(df['stale']) & (df['enabled'] == True), 'severity'] = 2

    # Disabled but still licensed (i.e. Account is disabled, but O365 license is live)
    df.loc[(df['enabled'] == False) & (df['licenseAssigned'] == True), 'severity'] = 3

    # Prioritize/Order by severity in remediation file 
    report = df[df['severity'] > 0].sort_values('severity', ascending=False)
    # POSSIBLE IMPROVEMENT: Flesh out severity level scaling/upgrades

    # Save discrepancies
    discrepancies_path = os.path.join(args.output_dir, 'discrepancies.csv')
    report.to_csv(discrepancies_path, index=False)

    # Generate remediation script
    remediation_path = os.path.join(args.output_dir, 'remediation.ps1')
    with open(remediation_path, 'w') as f:
        for _, r in report.iterrows():
            cmd = f"Disable-ADAccount -Identity ",{r['sAMAccountName']},"  # severity={r['severity']}"
            f.write(cmd if not args.dry_run else f"echo {cmd}")
    # POSSIBLE IMPROVEMENT: Workflows for each severity level, email admins for extreme severity 

    print(f"Report written to: {discrepancies_path}")
    print(f"Remediation script written to: {remediation_path}")

if __name__ == '__main__':
    main()
