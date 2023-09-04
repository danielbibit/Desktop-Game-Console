import pyWinCoreAudio

# devices = pyWinCoreAudio.devices(False)

# for device in devices():
for device in pyWinCoreAudio:
    print(device.name)
    print('    endpoints:')
    for endpoint in device:
        if endpoint.is_connected and endpoint.presence_detection:
            print('        endpoint: \'' + endpoint.name + '\'')
            print('        is_default:', endpoint.is_default)
            print('        guid:', endpoint.guid)
            print('        description:', endpoint.description)
            print('\n\n')


        del endpoint

    del device

pyWinCoreAudio.unload()
