
class MidiTieNotes(object):
    '''
    Helper class for handling tied notes when transcribing to midi.
    '''
    def __init__(self):
        self._note_time_elapsed = {}
        self._time_since_last_event = 0

    def _check_initialized(self, channel, note):
        if (channel, int(note)) not in self._note_time_elapsed:
            raise TiedNoteNotInitialized('Tied note %s was not initialized.' % str(note))

    def start(self, channel, note):
        '''
        Start tracking a tied note.
        '''
        self._note_time_elapsed[(channel, int(note))] = 0

    def advance(self, channel, note, dt):
        '''
        The tied note is played for another dt time.
        '''
        self._check_initialized(channel, note)
        self._note_time_elapsed[(channel, int(note))] += dt
        self._time_since_last_event += dt

    def elapsed(self, channel, note):
        '''
        Returns the time elapsed since the beginning of the tied note chain.
        '''
        self._check_initialized(channel, note)
        return self._note_time_elapsed[(channel, int(note))]

    def remaining(self, channel, note):
        '''
        At the last note in a tied chain, this returns the remaining deltatime.
        '''
        self._check_initialized(channel, note)
        return min(self._note_time_elapsed[(channel, int(note))], self._time_since_last_event)

    def stop(self, channel, note):
        '''
        End of a tied note.
        '''
        self._check_initialized(channel, note)
        del self._note_time_elapsed[(channel, int(note))]
        self._time_since_last_event = 0

    def touch(self):
        '''
        Called when an event is issued.
        '''
        self._time_since_last_event = 0


class TiedNoteNotInitialized(Exception):
    pass
