# Automated backups — schedule and recovery

Documents the backup automation the platform team set up. This is expected,
sanctioned automation.

## What runs

| Asset            | Tool                | Schedule (UTC)   | Retention |
|------------------|---------------------|------------------|-----------|
| Cloud SQL (prod) | automated PITR      | continuous       | 7 days    |
| Cloud SQL (prod) | daily full snapshot | 01:00 daily      | 30 days   |
| GCS user uploads | object versioning   | continuous       | 90 days   |
| Config/secrets   | Vault snapshot      | 02:00 daily      | 14 days   |

## Cron definitions

The daily snapshot is a Cloud Scheduler job (`pg-snapshot-prod`) that triggers a
Cloud Function. Crontab equivalent:

```
0 1 * * *   trigger pg-snapshot-prod   # daily full DB snapshot
0 2 * * *   trigger vault-snapshot      # daily Vault backup
0 4 * * 0   trigger backup-verify       # weekly restore test
```

## Verification

A weekly job restores the latest snapshot into a throwaway instance and runs a
row-count sanity check. If it fails, it pages the platform on-call. Backups you
can't restore aren't backups.

## Restoring (human-driven)

Restores are deliberately manual and require approval. Open an incident, pick the
snapshot timestamp, and run the documented `gcloud sql backups restore` against a
**new** instance first — never overwrite prod in place. The IC confirms before
any cutover.
