# HyperBackupFix

This Python script renames improperly created Synology Hyper Backup files for various reasons.
For instance, when backing up to Webdav using HyperBackup, files with the same name might be generated, as shown in the image below.

<img src="https://github.com/KimPig/HyperBackupFix/assets/61234733/f8452448-55c4-42b8-a87e-678f5b8a4455" alt="Example 1" width="600"/>

When viewed in Windows, these files appear with numbers like (2) appended to them.

![이미지 2024-07-05_19-28-24](https://github.com/KimPig/HyperBackupFix/assets/61234733/d7c286f9-c70d-4fe2-9288-b938507d606e)

This Python script detects duplicate filenames within a folder, retains the file with the largest size, and removes the others.

![이미지 2024-07-05_19-28-52](https://github.com/KimPig/HyperBackupFix/assets/61234733/cc547e40-06e5-404c-a79d-45fc689acd96)

**Warning**: Although this script has worked correctly for me, I cannot guarantee it will function properly in all scenarios. Please ensure you have a secondary backup before running this script.

## How to Use the Script

```bash
python fix.py "path"

