# Clear Disk database on new session.
Disk_Hardware.objects().delete()
cage = 0
'''
for d3940 in ov_disks:
    # Load server into mongo database
    for d in d3940['driveBays']:
        if d['drive']:

            # Build database entry to save creds
            drive = Disk_Hardware(serialNumber=d['drive']['serialNumber'].encode('utf-8'),
                                     model=d['drive']['model'].encode('utf-8'),
                                     rotationalRpms=str(d['drive']['rotationalRpms']),
                                     drivePaths=d['drive']['drivePaths'][0].encode('utf-8'),
                                     firmwareVersion=d['drive']['firmwareVersion'].encode('utf-8'),
                                     capacity=d['drive']['capacity'].encode('utf-8'),
                                     temperature=str(d['drive']['temperature']),
                                     blockSize=str(d['drive']['blockSize']),
                                     state=d['drive']['state'].encode('utf-8'),
                                     deviceInterface=d['drive']['deviceInterface'].encode('utf-8'),
                                     status=d['drive']['status'].encode('utf-8'),
                                     driveMedia=d['drive']['driveMedia'].encode('utf-8'),
                                     authentic=d['drive']['authentic'].encode('utf-8'),
                                     cage=str(cage))

            # Save the record
            try:
                drive.save()
            except:
                error="SUB-SUB routine- ERR00100 - Failed to save server_harware"
                return render_template('main/dberror.html', error=errors)
    cage = cage + 1
'''
