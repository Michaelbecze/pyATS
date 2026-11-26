import sys
from genie.testbed import load
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from dotenv import load_dotenv

load_dotenv() 

def is_up(entry):
    if 'status' in entry:
        return entry['status'] == 'up' and entry.get('protocol') == 'up'

def check_addressing(testbed):
    testbed = load(testbed)
    problems = []

    for name, device in testbed.devices.items():
        device.connect(log_stdout=False, init_config_commands=[])

        try:
            actual = device.parse('show ip interface brief')['interface']
        except SchemaEmptyParserError:
            problems.append(f'{name}: no interfaces returned')
            continue

        for intf_name, intf in device.interfaces.items():
                entry = actual.get(intf_name)
                continue                       

        if not is_up(entry):
                problems.append(f'{name} {intf_name}: not up '
                                f'(status={entry.get("status")}, '
                                f'protocol={entry.get("protocol")})')
                
        intended = getattr(intf, 'ipv4', None)
        if intended is not None:
            seen = entry.get('ip_address')
            if seen != str(intended.ip):
                problems.append(
                    f'{name} {intf_name}: expected {intended.ip}, found {seen}')

        device.disconnect()

    return problems


if __name__ == '__main__':
    issues = check_addressing(sys.argv[1])
    for issue in issues:
        print('FATAl ERROR', issue)
    print(f'{len(issues)} problem(s)')
    sys.exit(1 if issues else 0)