# -*- coding: utf-8 -*-
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#
#
# Ice version 3.7.10
#
# <auto-generated>
#
# Generated from file `AudioStream.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy

# Start of module YourModule
_M_YourModule = Ice.openModule('YourModule')
__name__ = 'YourModule'

_M_YourModule._t_AudioStream = IcePy.defineValue('::YourModule::AudioStream', Ice.Value, -1, (), False, True, None, ())

if 'AudioStreamPrx' not in _M_YourModule.__dict__:
    _M_YourModule.AudioStreamPrx = Ice.createTempClass()
    class AudioStreamPrx(Ice.ObjectPrx):

        def playAudio(self, context=None):
            return _M_YourModule.AudioStream._op_playAudio.invoke(self, ((), context))

        def playAudioAsync(self, context=None):
            return _M_YourModule.AudioStream._op_playAudio.invokeAsync(self, ((), context))

        def begin_playAudio(self, _response=None, _ex=None, _sent=None, context=None):
            return _M_YourModule.AudioStream._op_playAudio.begin(self, ((), _response, _ex, _sent, context))

        def end_playAudio(self, _r):
            return _M_YourModule.AudioStream._op_playAudio.end(self, _r)

        @staticmethod
        def checkedCast(proxy, facetOrContext=None, context=None):
            return _M_YourModule.AudioStreamPrx.ice_checkedCast(proxy, '::YourModule::AudioStream', facetOrContext, context)

        @staticmethod
        def uncheckedCast(proxy, facet=None):
            return _M_YourModule.AudioStreamPrx.ice_uncheckedCast(proxy, facet)

        @staticmethod
        def ice_staticId():
            return '::YourModule::AudioStream'
    _M_YourModule._t_AudioStreamPrx = IcePy.defineProxy('::YourModule::AudioStream', AudioStreamPrx)

    _M_YourModule.AudioStreamPrx = AudioStreamPrx
    del AudioStreamPrx

    _M_YourModule.AudioStream = Ice.createTempClass()
    class AudioStream(Ice.Object):

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::YourModule::AudioStream')

        def ice_id(self, current=None):
            return '::YourModule::AudioStream'

        @staticmethod
        def ice_staticId():
            return '::YourModule::AudioStream'

        def playAudio(self, current=None):
            raise NotImplementedError("servant method 'playAudio' not implemented")

        def __str__(self):
            return IcePy.stringify(self, _M_YourModule._t_AudioStreamDisp)

        __repr__ = __str__

    _M_YourModule._t_AudioStreamDisp = IcePy.defineClass('::YourModule::AudioStream', AudioStream, (), None, ())
    AudioStream._ice_type = _M_YourModule._t_AudioStreamDisp

    AudioStream._op_playAudio = IcePy.Operation('playAudio', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), None, ())

    _M_YourModule.AudioStream = AudioStream
    del AudioStream

# End of module YourModule
