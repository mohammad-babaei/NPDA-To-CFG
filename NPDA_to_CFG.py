class NPDA:
    def __init__(self, StateCount=None, alphabet=None, stackSigns=None, stackFirstSign=None, connections=[]):
        self.StateCount = StateCount
        self.alphabet = alphabet
        self.stackSigns = stackSigns
        self.stackFirstSign = stackFirstSign
        self.connections = connections
        self.initialState = ""
        self.finalState = ""
        self.states = []
        self.cfg_rules=[]

    def init_npda(self, input_txt):

        for line in input_txt:

            input_line = line.replace("\n", "")

            if input_txt.index(line) == 0:
                npda.StateCount = int(input_line)
            elif input_txt.index(line) == 1:
                npda.StateCount = input_line.split(",")
            elif input_txt.index(line) == 2:
                npda.stackSigns = input_line
            elif input_txt.index(line) == 3:
                npda.stackFirstSign = input_line
            else:
                npda.connections.append(input_line)
        self.set_initial_state()
        self.set_states()

    def set_states(self):
        for connection in self.connections:
            states = [connection.split(",")[0], connection.split(",")[len(connection.split(","))-1]]

            for state in states:
                naked_state = state.replace("*", "").replace("->", "")
                if "->" in state and naked_state not in self.states:
                    self.states.append(naked_state)
                if "*" in state and naked_state not in self.states:
                    self.states.append(naked_state)
                elif naked_state not in self.states:
                    self.states.append(naked_state)

    def set_initial_state(self):
        for connection in self.connections:
            line = connection.split(",")
            for state in line:
                if "->" in state:
                    self.initialState = state.replace("*", "").replace("->", "")
                if "*" in state:
                    self.finalState = state.replace("*", "").replace("->", "")
    
    
    def connection_to_rules(self):
        for connection in self.connections:
            line = [x.replace("*","").replace("->","") for x in connection.split(",")]
            first_state = line[0]
            next_state = line[4]
            alphabet = line[1]
            pop_element = line[2]
            push_element = line[3]
        
        
            if push_element == "_":
                data = (first_state,pop_element,next_state,alphabet)
                rule = "(%s%s%s) -> %s" % data
                self.cfg_rules.append(rule)
            else:
                for qk in self.states:
                    for ql in self.states:
                        data = (first_state,pop_element,qk,alphabet,next_state,push_element[0],ql,ql,push_element[1],qk)
                        rule = "(%s%s%s) -> %s(%s%s%s)(%s%s%s)" % data
                        self.cfg_rules.append(rule)
        
        self.cfg_rules = list(set(self.cfg_rules))
        




if __name__ == "__main__":
    input_file = open("input.txt", "r")
    input_txt = input_file.readlines()

    npda = NPDA()
    npda.init_npda(input_txt)
    npda.connection_to_rules()
    output = open("CFG.txt",'w')
    output.write('\n'.join(npda.cfg_rules))
    output.write('\n'+'('+npda.initialState+'$'+npda.finalState+')')
    output.close()
