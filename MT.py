class MT():
    def __init__(self, config):
        # Propriedades da MT
        self.sigma = []
        self.gamma = []
        self.qAceita = []
        self.q0 = 0
        self.qRejeita = []
        self.q = []
        self.delta = {}

        self.testWords = []

        #Le arquivo
        content = []
        with open(config, 'r') as f:
            content = f.readlines()

        # 1 - Le os elementos do alfabeto de entrada;
        line = 0
        for c in content[line].rstrip('\n'):
            self.sigma.append(c)
        # Copia os elementos de entrada para o de fita (pq estão concatenados) e adiciona o simbolo vazio
        self.gamma = self.sigma.copy() + ['-']

        # 2 - Le a qtd de estado e seta o inicial e de aceitação;
        line += 1
        self.q = [q+1 for q in range(int(content[line]))]
        self.q0 = self.q[0]
        self.qAceita = self.q[-1]

        # 3 - Le a qtd de transições;
        line += 1
        numTransition = int(content[line])
        # Cada transição e coloca no dict no esquema EstadoLeitura, onde leitura é o que se le da fita
        for i in range(3, 3 + numTransition):
            t = content[i].rstrip("\n").split(" ")
            self.delta[f"{t[0]}{t[1]}"] = t[2:]

        # 4 - Le o numero de palavras e coloca no array;
        line += numTransition + 1
        numWords = int(content[line])
        for i in range(line+1, line + numWords+1):
            self.testWords.append(content[i].rstrip("\n"))
    
    # Func para printar a configuração da MT
    def showConfig(self):
        print(f"Sigma: {self.sigma}")
        print(f"Gamma: {self.gamma}")
        print(f"Q : {self.q}")
        print(f"q0 : {self.q0}")
        print(f"qAceita : {self.qAceita}")
        print(f"qRejeita : {self.qRejeita}")
        print(f"Delta: {self.delta}")
        print(f"Words: {self.testWords}")

    # Func para executar o simulador
    def run(self):
        #Para cada palavra de teste
        for index, word in enumerate(self.testWords):
            # Cabeçote na primeira posição
            pointer = 0
            # Carrega a fita
            tape = ["-" for i in range(100)]
            # Copia a palavra para fita
            for i in range(len(word)):
                tape[i] = word[i]
            
            # Estado initial
            q = self.q0
            
            # Execução
            running = True
            while(running):
                # Le o caractere da onde o cabeçote está
                read = tape[pointer]
                # Se o EstadoLeitura estiver no dict, ou seja, se a transição existir
                if f"{q}{read}" in self.delta.keys():
                    # Pega os próximos passos: Escrita, Direção, Prox Estado
                    write, direction, nextState = self.delta[f"{q}{read}"]
                    # Escreve
                    tape[pointer] = write
                    # Move
                    pointer += 1 if direction == "D" else -1
                    # Muda o estado
                    q = nextState
                else: # Se a transição não for possível
                    # Se ele está no estado final, Aceite
                    if int(q) == self.qAceita:
                        running = False
                        print(f"{index + 1}: {word} OK")
                    else: # Caso contrário, Rejeite
                        running = False
                        print(f"{index + 1}: {word} not OK")
