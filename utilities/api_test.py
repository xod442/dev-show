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
ov = client.appliance_node_information.get_version()
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

'''
for k, v in ov.iteritems():
    print(v)
    print "---------------------------------------------------------------"
'''
