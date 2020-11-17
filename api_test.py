from hpOneView.oneview_client import OneViewClient
authx = {
    "ip" : "10.132.0.3",
    "credentials" : {
        "userName" : "Administrator",
        "password" : "orange123"
    }
}

client = OneViewClient(authx)
# Call api
# ov = client.alerts.get_all()
# ov = client.appliance_node_information.get_status()
# #ov = client.appliance_node_information.get_version()
# ov_servers = client.server_hardware.get_all()
ov_disks = client.drive_enclosures.get_all()
'''
# Print ov_alerts
print(ov['build'])
print(type(ov))
print(len(ov))
uuid=ov['uuid'].encode('utf-8')
family=ov['family'].encode('utf-8')
serno=ov['serialNumber'].encode('utf-8')
model=ov['modelNumber'].encode('utf-8')
software=ov['softwareVersion'].encode('utf-8')
build=ov['build'].encode('utf-8')
out=[uuid,family,serno,model,software,build]
print(out)


print(ov)
D3940_number = len(ov)
count = D3940_number - 1
# print(ov[0]['driveEnclosureLocation'])
print('@@@@@@@@@@@')
print(ov[count]['driveBays'][count]['driveBayLocation']['locationEntries'][0]['type'])
print(ov[count]['driveBays'][count]['driveBayLocation']['locationEntries'][0]['value'])
print(ov[count]['driveBays'][count]['category'])
print(ov[count]['driveBays'][count]['drive'])
print(ov[count]['driveBays'][count]['drive']['rotationalRpms'])
# print(ov[0]['locationEntries'])
x=ov[count]['driveBays']
print('+++++++++++++++++++++++++++++++++++++')
for d in x:
    if d['drive']:

        print(d)
        print('+++++++++++++++++++++++++++++++++++++')
print(len(ov))
'''
cage = 0
for d3940 in ov_disks:
    # Load server into mongo database
    for d in d3940['driveBays']:
        if d['drive']:

            # Build database entry to save creds
            serialNumber=d['drive']['serialNumber'].encode('utf-8')
            model=d['drive']['model'].encode('utf-8')
            rotationalRpms=str(d['drive']['rotationalRpms'])
            drivePaths=d['drive']['drivePaths']
            firmwareVersion=d['drive']['firmwareVersion'].encode('utf-8')
            capacity=d['drive']['capacity'].encode('utf-8')
            temperature=d['drive']['temperature']
            blockSize=d['drive']['blockSize']
            state=d['drive']['state'].encode('utf-8')
            deviceInterface=d['drive']['deviceInterface'].encode('utf-8')
            status=d['drive']['status'].encode('utf-8')
            driveMedia=d['drive']['driveMedia'].encode('utf-8')
            authentic=d['drive']['authentic'].encode('utf-8')
            out = [serialNumber,model,rotationalRpms,drivePaths,firmwareVersion,capacity,temperature,blockSize,state,deviceInterface,status,driveMedia,authentic,cage]
            print('+++++++++++++++++++++++++++++++++++++')
            print(out)
            print('+++++++++++++++++++++++++++++++++++++')
    cage = cage + 1
