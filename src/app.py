import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Automation Demo")
        layout = QVBoxLayout()

        self.output = QTextEdit(readOnly=True)
        button = QPushButton("Run Measurement")
        button.clicked.connect(self.run_measurement)

        layout.addWidget(button)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def run_measurement(self):
        self.output.append("Running measurement...")
        self.output.append("Result: 1.0 ± 0.05\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())
