"""fsa.py

Separate module to store most FSA related code.


"""

class FSA(object):
    
    """Class to implement a simple deterministic FSA."""
    
    def __init__(self, name, states, final_states, transitions):
        """Initialize with a set of states, final states and transitions."""
        self.name = name
        self.states = {}
        for state_name in states:
            state = State(state_name)
            if state_name in final_states:
                state.is_final = True
            self.states[state_name] = state
        for s1, label, s2 in transitions:
            self.states[s1].transitions[label] = self.states[s2]
            
    def __str__(self):
        return "<FSA with %d states>" % len(self.states)

    def pp(self):
        print('<FSA "%s">' % self.name)
        for state_symbol in sorted(self.states):
            state = self.states[state_symbol]
            print('  ', state)
            for symbol, target in state.transitions.items():
                # U+27f6 = 'LONG RIGHTWARDS ARROW'
                print('      %s \u27f6 %s' % (symbol, target.name))

    def print_state(self, indent=0, debug=True):
        if debug:
            print("%s%s %s . %s" % (' ' * indent, self.current_state, 
                                    ' '.join(self.consumed), ' '.join(self.queue[:5])))

    def consume(self, sequence, debug=False):
        """Given a sequence, consume as many vocabulary elements from the beginning as
        possible. Returns a Match instance if input was consumed or False if no match
        was found."""
        self.input_tape = sequence
        self.queue = list(sequence)
        self.consumed = []
        self.current_state = self.states['S0']
        # storing the longest match if there is a match
        self.match = False
        self.print_state(indent=3, debug=debug)
        while self.queue:
            next_symbol = self.queue.pop(0)
            if next_symbol in self.current_state.transitions:
                self.current_state = self.current_state.transitions[next_symbol]
                self.consumed.append(next_symbol)
                if self.current_state.is_final:
                    self.match = Match(self)
            else:
                break
            self.print_state(indent=3, debug=debug)
        return self.match
        
    def accept(self, sequence):
        """Returns True if a full match for the sequence was found, False otherwise."""
        match = self.consume(sequence)
        # simply check whether the match was for the full sequence
        return match and len(match.consumed) == len(sequence)


class State(object):

    """Each State has a name and a dictionary of transitions indexed on vocabulary
    elements with names of states as values."""

    def __init__(self, name):
        self.name = name
        self.transitions = {}
        self.is_final = False

    def __str__(self):
        final =  ' f' if self.is_final else ''
        return "<State %s%s>" % (self.name, final)


class Match(object):

    """The Match object is initialized from an FSA and simply keeps a copy of the
    sequence consumed."""
    
    def __init__(self, fsa):
        self.consumed = fsa.consumed[:]
        
    def __str__(self):
        return ' '.join(self.consumed)
    
    def __len__(self):
        return len(self.consumed)


if __name__ == '__main__':

    states = ['S0', 'S1', 'S2']
    final_states = ['S2']
    transitions = [ ('S0', 'a', 'S1'), ('S1', 'b', 'S1'), ('S1', 'c', 'S2') ]
    fsa_abc = FSA('test', states, final_states, transitions)

    print()
    fsa_abc.pp()

    print("\nTesting some strings...\n")
    for s in ('abc', 'ab', 'abbc', 'abcd'):
        print("   %-5s" % s, end='')
        print(' ', fsa_abc.accept(s))

    print("\nConsuming as much as possible from abbcd...\n")
    fsa_abc.consume('abbcd', debug=True)
