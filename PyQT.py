import sys
from PyQt5.QtWidgets import *

test_text = '''
data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 11.693231582641602
Answer: rewards
Context: assign rewards in a way that causes undesirable behavior for this example. one mistake is to give positive rewards for walking on the sidewalk — in that case the agent will learn to walk back and forth on the sidewalk gathering more and more rewards, rather than going to the door where the episode ends. in this case, optimal behavior is produced by putting negative rewards on the flowerbed, and a positive reward at the door. this provides a general rule of thumb when designing rewards : give rewards for what you want the agent to achieve, not for how you think the agent should achieve it. rewards that are given to help the agent quickly

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.994667053222656
Answer: s0
Context: a single state, s0, that self - transitions with probability 0. 5, and transitions to s∞with probability 0. 5. let γ = 1. let the reward be + 1 for self - transitions, and 0 for transitioning to s∞. the value of s0in the example is 1, and the expected return from the first visit to s0is 1. however, if we compute the expected return from the lastvisit to s0, it is zero. next consider the expected return if we only consider returns from the second time that sis visited in each trajectory. by the markov property, what happened

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.985766410827637
Answer: sign change in the last term is to obtain a standard form
Context: gradient : ∂ ∂wl ( w ) = ∂ ∂we1 2 ( rt + γvw ( st + 1 ) −vw ( st ) ) 2 ( 230 ) = e δt γ∂vw ( st + 1 ) ∂w−∂vw ( st ) ∂w ( 231 ) = e −δt∂vw ( st ) ∂w−γ∂vw ( st + 1 ) ∂w, ( 232 ) where the sign change in the last term is to obtain a standard form. this suggests a stochastic gradient descent update ( notice that the negative from this being a descent algorithm cancel

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.854403495788574
Answer: skill characterization
Context: icml, 2014. o. simsek and a. barto. skill characterization based on betweenness. in proceedings of the 22nd annual conference on neural information processing systems, vancouver, b. c, canada, december 2008. 113 s. singh, t. jaakkola, m. l. littman, and c. szepesv´ ari. convergence results for single - step on - policy reinforcement - learning algorithms. machine learning, 38 ( 3 ) : 287 – 308, 2000. a. l. strehl, l. li, e. wiewiora, j. langford, and

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.753617286682129
Answer: reward signal
Context: , software environment, etc. the semester. for now, a brief overview : in this animal / psychology / neuroscience setting rewards refer to something given to an agent that is rewarding, like food. this is translated in the animal ’ s brain into a reward signal. this reward signal could, for example, correspond to the firing of specific neurons or the release of a specific neurotransmitter. using this terminology, our rtcorresponds to the reward signal in the animal ’ s brain rather than the reward ( say, a cookie ). some function defines how reward signals are generated within the brain when an agent receives

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.666143417358398
Answer: 54 5. 2 a gradient - based monte carlo algorithm.............
Context: .. 54 5. 2 a gradient - based monte carlo algorithm............. 59 6 temporal differenence ( td ) learning 61 6. 1 function approximation....................... 65 6. 2 maximum likelihood model of an mdp versus temporal differ - ence learning............................. 66 7 sarsa : using td for control 67 8q - learning : off

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.61246109008789
Answer: eligibility
Context: eligibility traces is not a feature, but an unfortunate consequence of using experience replay ( mnih et al., 2015 ). papers have begun to address the question of how to perform experience replay in a principled manner with λ - returns ( daley and amato, 2019 ). 13. 3 multi - agent reinforcement learning multi - agent reinforcement learning ( marl ) involves a set of agents acting in the same environment, where the actions of one agent can impact the states and rewards as seen by other agents. research has studied both cooperative problems, wherein all of the agents obtain the same rewards, and thus work together, as well as

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.540620803833008
Answer: agent always begins ins0, and walks down the line of states
Context: 10cookies figure 10 : the “ cookie mdp ”. under some policy, π, the agent always begins ins0, and walks down the line of states. the agent receives a reward of + 1 when transitioning from state s0tos1and a reward of + 10 when transitioning from s2tos3. all other transitions result in a reward of zero. similarly, we can compute vπ ( s1 ) using the definition of the value function or the bellman equation : vπ ( s1 ) = r1 + γr2 + γ2r3 = 0 + γ10 + γ20 =

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.527315139770508
Answer: e [ rt | st = s, π ] + γe
Context: ] ( 58 ) = e [ rt | st = s, π ] + γe [ rt + 1 | st = s, π ] + γ2e [ rt + 2 | st = s, π ] + · · · ( 59 ) = x a∈apr ( at = a | st = s, π ) e [ rt | st = s, at = a, π ] ( 60 ) + γx a∈apr ( at = a | st = s, π ) x s ′ ∈spr ( st + 1 = s ′ | st = s, at = a, π ) (

data_directory2/Lecture_Notes_v1.0_687_F22.pdf - 10.4984712600708
Answer: train
Context: 4 a = agent. getaction ( s ) ; 5 s ′ [UNK] ( s, a, · ) ; 6 [UNK] ( s, a, s ′ ) ; 7 agent. train ( s, a, r, s ′ ) ; 8 ifs ′ = = s∞then 9 break ; / / exit out of loop over time, t 10 s = s ′ ; 11 agent. newepisode ( ) ; here the agent has three functions. the first, getaction, which samples an action, a, given the current state s, and using the agent ’ s current policy. the second function
'''

class EmbeddingApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 240
        self.currentPath = ""
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()

        self.textWindow = QLabel()
        layout.addWidget(self.textWindow, 0, 0, 1, 2)
		
        self.filepathBox = QLineEdit(self, readOnly=True, placeholderText="...")
        layout.addWidget(self.filepathBox, 1, 0)


        self.btn1 = QPushButton("Select a File")
        self.btn1.clicked.connect(self.folderDialog)
        layout.addWidget(self.btn1, 1, 1)

        self.saveFileName = QLineEdit(self, placeholderText="Embedding file name")
        layout.addWidget(self.saveFileName, 2, 0)

        self.btn2 = QPushButton("Create Embedding")
        self.btn2.clicked.connect(self.execute)
        layout.addWidget(self.btn2, 2,1)
        
        self.setLayout(layout)
        
        self.show()
    def folderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,"QFileDialog.getExistingDirectory()", self.currentPath, options=options)
        if directory:
            self.filepathBox.setText(directory)
    def execute(self):
        self.textWindow.setText("Embeddings being created and saved to " + self.saveFileName.text() + ".json")

class SearchApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs'
        self.left = 10
        self.top = 10
        self.width = int(640*1.5)
        self.height = int(480*1.5)
        self.currentPath = ""
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()

        self.textWindow = QTextBrowser(self, readOnly=True)

        layout.addWidget(self.textWindow, 0, 0, 1, 2)
		
        self.filepathBox = QLineEdit(self, readOnly=True, placeholderText="...")
        layout.addWidget(self.filepathBox, 1, 0)


        self.btn1 = QPushButton("Select a File")
        self.btn1.clicked.connect(self.folderDialog)
        layout.addWidget(self.btn1, 1, 1)

        self.saveFileName = QLineEdit(self, placeholderText="Search text...")
        layout.addWidget(self.saveFileName, 2, 0)

        self.btn2 = QPushButton("Search")
        self.btn2.clicked.connect(self.execute)
        layout.addWidget(self.btn2, 2,1)
        
        self.setLayout(layout)
        
        self.show()
    def folderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,"QFileDialog.getExistingDirectory()", self.currentPath, options=options)
        if directory:
            self.filepathBox.setText(directory)
            self.textWindow.setPlainText("File loaded \nReady to search")
    def execute(self):
        self.textWindow.setPlainText(test_text)

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle("Fusion")

    try:
        if sys.argv[1] == "search":
            ex = SearchApp()
        else:
            ex = EmbeddingApp()
    except:
        ex = EmbeddingApp()
    sys.exit(app.exec())
