class node:
    def __init__(self,name,right_sides):
        self.name = name
        self.childs = []
        self._childSetter(right_sides)

    def _childSetter(self,right_sides):
        for i in right_sides:
            self.childs.append(i)




class Tracker:
    def __init__(self,rules,root_name):
        self.rules = self._rules_corrector(rules)
        self.root = self._initNode(root_name)
        self.nodes = {root_name:self.root}
        self._initNodes()
        self.alphabet = []
        self._init_alph()
        self.Readable_rules = []
        self._init_Readable_rules()
    
    def _init_Readable_rules(self):
        a = {}
        for i in self.nodes.values():
            for j in i.childs:
                self.Readable_rules.append(tuple(j))
                if(')' in j[1]):
                    slides = j[1].split('(')
                    slides[1] = '('+slides[1]
                    slides[2] = '('+slides[2]
                    if(slides[1] not in self.nodes.keys()):
                        a[slides[1]] = ""
                    if(slides[2] not in self.nodes.keys()):
                        a[slides[2]] = ""

        self.nodes.update(a)
                        


    def _init_alph(self):
        for i in self.rules:
            sides = i.split(" -> ")
            if('(' not in sides[1]):
                self.alphabet.append(sides[1])

        
    def _rules_corrector(self,rules):
        for i in range(len(rules)-1):
            sides = rules[i].split(" -> ")
            sides[0] = sides[0].replace(' ', '')
            sides[1] = sides[1].replace(' ', '')
            sides[1] = sides[1].replace('\n', '')
            rules[i] = " -> ".join(sides)
        return list(set(rules))    

    def _initNode(self,node_name):
        right_sides = []
        for rule in self.rules:
            if(node_name in rule):
                right_side = rule.split(" -> ")
                right_sides.append(right_side)
        return node(node_name,right_sides)
    def _initNodes(self):
        for i in self.rules:
            sides = i.split(" -> ")
            if(sides[0] not in self.nodes.keys()):
                self.nodes[sides[0]]=self._initNode(sides[0])


if __name__ == "__main__":
    in_file = open("CFG.txt",'r')
    rules = in_file.read().split('\n')
    root_name = rules.pop()
    tracker = Tracker(rules,root_name)

    from cfg import CFG

    g = CFG(set(tracker.nodes.keys()), set(tracker.alphabet+['_']),set(tracker.Readable_rules), tracker.root.name, '_')

    string = input("Enter a string: ")

    if g.cyk(string):
        print("Grammar can generate the string!")
    else:
        print("Grammar cannot generate the string!")