from pyVim import connect
from pyVmomi import vim
from datetime import datetime
from colorama import Fore, Style
import argparse
import sys
from getpass import getpass

argParser = argparse.ArgumentParser(description='You must specify hostname and credentials.')  # noqa: E501
argParser.add_argument("-u", "--username", help="Login username (user@vsphere.local)",required=True)
argParser.add_argument("-x", "--hostname", help="VCSA HOSTNAME (vcsa.domain.local)", required=True)

if len(sys.argv)==1:
    argParser.print_help(sys.stderr)
    sys.exit(1)
    
args = argParser.parse_args()

vcenter_host = f"{args.hostname}"
vcenter_user = f"{args.username}"
vcenter_password = getpass(prompt='Enter your password (Do not use CTRL+V on Windows): ')

def get_snapshot_count(snapshot):
    if snapshot.childSnapshotList:
        count = 0
        for child_snapshot in snapshot.childSnapshotList:
            count += 1 + get_snapshot_count(child_snapshot)
        return count
    else:
        return 0

def get_vm_snapshots(vcenter_host, vcenter_user, vcenter_password, vcenter_port=443):
    try:
        service_instance = connect.SmartConnect(
            host=vcenter_host,
            user=vcenter_user,
            pwd=vcenter_password,
            port=vcenter_port,
            disableSslCertValidation=True
        )

        content = service_instance.RetrieveContent()

        vm_snapshots = []
        container_view = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )

        for vm in container_view.view:
            vm_moid = vm._moId
            vm_name = vm.name

            if vm.snapshot is not None and vm.snapshot.rootSnapshotList is not None:
                snapshots = vm.snapshot.rootSnapshotList
                for snapshot in snapshots:
                    create_time = datetime.strftime(snapshot.createTime, "%Y-%m-%d %H:%M:%S")
                    snapshot_count = get_snapshot_count(snapshot)
                    snapshot_info = {
                        'VM Name': vm_name,
                        'VM MoID': vm_moid,
                        'Snapshot Name': snapshot.name,
                        'Snapshot MoID': snapshot.snapshot._moId,
                        'Creation Time': create_time,
                        'Snapshot Count': snapshot_count
                    }
                    vm_snapshots.append(snapshot_info)

        connect.Disconnect(service_instance)

        return vm_snapshots

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
vm_snapshots = get_vm_snapshots(vcenter_host, vcenter_user, vcenter_password)

if vm_snapshots:

    for snapshot in vm_snapshots:
        output = f"{Fore.RED + snapshot['VM Name'] + Style.RESET_ALL} → Root snapshot: {Fore.LIGHTBLUE_EX + snapshot['Snapshot Name'] + Style.RESET_ALL} with creation time: {Fore.YELLOW + snapshot['Creation Time'] + Style.RESET_ALL} ■ Total snapshots: {snapshot['Snapshot Count'] + 1}"
        print(output)

else:
    exit