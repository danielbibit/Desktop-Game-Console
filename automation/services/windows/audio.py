import pyWinCoreAudio
class Audio:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def set_default(mode: str, ident: str):
        try:
            for device in pyWinCoreAudio:
                for endpoint in device:
                    if (mode == 'guid' and endpoint.guid == ident) or (mode == 'name' and endpoint.name == ident):
                        endpoint.set_default(0)
                        endpoint.set_default(1)
                        endpoint.set_default(2)

                    del endpoint

                del device

            pyWinCoreAudio.stop()
        except Exception:
            pass


    def set_default_external(self):
        self.set_default('guid', self.config['default_audio_external'])


    def set_default_internal(self):
        self.set_default('guid', self.config['default_audio_pc'])
