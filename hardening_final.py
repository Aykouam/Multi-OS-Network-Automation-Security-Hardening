import paramiko
import os
from datetime import datetime
from netmiko import ConnectHandler

# --- LEGACY SSH FIX FOR .35 (IOS-XRv) ---
try:
    paramiko.Transport._preferred_keys = ('ssh-ed25519', 'ssh-rsa', 'ssh-dss')
except Exception:
    pass

# --- CONFIGURATION VARIABLES (REDACTED FOR GITHUB) ---
USER_NAME = "Aluko"
NEW_SSH_PW = "REDACTED_SECURE_PASSWORD" 
BACKUP_DIR = "network_backups"

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# --- MULTI-OS DEVICE DEFINITIONS ---
devices = [
    {
        'device_type': 'cisco_ios', 'host': '10.10.20.48', 'un': 'developer', 'pw': 'REDACTED',
        'name': 'Catalyst 8000',
        'cmds': [
            'service password-encryption',
            f'username developer secret {NEW_SSH_PW}',
            'enable secret class',
            f'banner motd # Welcome {USER_NAME}! Connected to $(hostname) #',
            f'banner exec # Authorized Access: {USER_NAME} | Line: $(line) #'
        ]
    },
    {
        'device_type': 'cisco_xr', 'host': '10.10.20.35', 'un': 'developer', 'pw': 'REDACTED',
        'name': 'IOS XRv 9K',
        'cmds': [
            f'username developer secret {NEW_SSH_PW}',
            f'banner motd # Welcome {USER_NAME}! Connected to $(hostname) #',
            f'banner exec # Authorized Access: {USER_NAME} #'
        ]
    },
    {
        'device_type': 'cisco_nxos', 'host': '10.10.20.40', 'un': 'admin', 'pw': 'REDACTED',
        'name': 'Nexus9k',
        'cmds': [
            f'username developer password {NEW_SSH_PW}',
            f'banner motd # Welcome {USER_NAME}! Connected to $(hostname) #',
            f'banner exec # Authorized Access: {USER_NAME} #'
        ]
    }
]

def backup_config(link, name, ip):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{BACKUP_DIR}/{name.replace(' ', '_')}_{timestamp}.txt"
    try:
        config = link.send_command('show running-config')
        with open(filename, "w") as f:
            f.write(config)
        print(f"   [+] Backup successful: {filename}")
    except Exception as e:
        print(f"   [!] Backup failed for {name}: {e}")

for dev in devices:
    print(f"\n--- Processing Node: {dev['name']} ({dev['host']}) ---")
    for trial_pw in [dev['pw'], NEW_SSH_PW]:
        try:
            conn_params = {'device_type': dev['device_type'], 'host': dev['host'], 'username': dev['un'], 'password': trial_pw, 'global_delay_factor': 2}
            with ConnectHandler(**conn_params) as link:
                backup_config(link, dev['name'], dev['host'])
                link.send_config_set(dev['cmds'])
                if dev['device_type'] == 'cisco_xr': link.commit()
                else: link.send_command_timing('copy run start')
                print(f"   [!] SUCCESS: {dev['name']} Hardened and Backed Up.")
                break
        except Exception: continue
print("\n--- Full-Fleet Automation Complete ---")
