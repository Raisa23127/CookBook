import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("РАБОТАЕТ!")
window.resize(400, 200)

layout = QVBoxLayout()

label = QLabel("✅ ВСЁ ХУЯРИТ!")
label.setStyleSheet("font-size: 24px; color: green; font-weight: bold;")

button = QPushButton("ЖМИ СЮДА")
button.setStyleSheet("""
    QPushButton {
        background-color: blue;
        color: white;
        font-size: 18px;
        padding: 15px;
    }
""")

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)
window.show()

sys.exit(app.exec())