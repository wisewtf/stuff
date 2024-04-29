# Snapshot Shield

This script will read information about VM snapshots using VMWare's [vCenter API](https://developer.vmware.com/apis/vsphere-automation/latest/vcenter/) through [pyvmomi](https://github.com/vmware/pyvmomi).

## How to use

- Install libraries from `requirements.txt` using `pip`. ([How to](https://stackoverflow.com/a/15593865))
- Use Python 3 to launch it from the command line, for example: `python .\snapshotshield.py  -u Administrator@vsphere.local -x your.vcsa.hostname.com`.

```shell
usage: snapshotshield.py [-h] -u USERNAME -x HOSTNAME

You must specify hostname and credentials.

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Login username (user@vsphere.local)
  -x HOSTNAME, --hostname HOSTNAME
                        VCSA HOSTNAME (vcsa.domain.local)
```

- Input your password. **Pay attention not to use `CTRL+V` on Windows machines as `getpass` inputs a specific character with that keyboard combination. (<https://bugs.python.org/issue37426>)**
