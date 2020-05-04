class OutputCea:
    def __init__(self, rockets):
        self.rockets=rockets

    def make(self):
         for rocketName, rocketData in self.rockets.items():
             for block in rocketData:
                 if block['type']=='liquid':
                     output=block['solvedData']['full_output_cea'].getValue()[0].output
                     f = open('out/cea/' + block['name'].replace(' ', '_') + '_' + block['engName'].replace(' ', '_') + '.txt', 'w+')
                     f.write(output)
                     f.close()
