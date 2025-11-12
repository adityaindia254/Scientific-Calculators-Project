import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from calc import calculate_basic
from graphing import GraphWidget
from postfix import infix_to_postfix


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setStyleSheet(self.load_light_theme())

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_calculator_tab(), "Calculator")
        self.tabs.addTab(self.create_postfix_tab(), "Infix → Postfix")
        self.tabs.addTab(self.create_graphing_tab(), "Graphing")
        self.tabs.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        modifiers = event.modifiers()

        # Get active tab and its input
        tab_idx = self.tabs.currentIndex()
        input_field = None
        if tab_idx == 0:
            input_field = self.calc_input
        elif tab_idx == 1:
            input_field = self.postfix_input
        elif tab_idx == 2:
            input_field = self.graph_input

        # Enter = Evaluate
        if key in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
            if tab_idx == 0:
                self.run_calculator()
            elif tab_idx == 1:
                self.run_postfix()
            elif tab_idx == 2:
                self.graph_plot()
            return

        # Ctrl+Backspace = Clear
        if (
            key == Qt.Key.Key_Backspace
            and modifiers == Qt.KeyboardModifier.ControlModifier
        ):
            if input_field:
                input_field.clear()
            return

        # Ctrl+1/2/3 = Tab switch
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            if key == Qt.Key.Key_1:
                self.tabs.setCurrentIndex(0)
            elif key == Qt.Key.Key_2:
                self.tabs.setCurrentIndex(1)
            elif key == Qt.Key.Key_3:
                self.tabs.setCurrentIndex(2)
            return

        super().keyPressEvent(event)

    def create_button_grid(self, target_input):
        grid = QGridLayout()

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "(", ")"],
            ["C", "←", "+", "="],
        ]

        for row, line in enumerate(buttons):
            for col, btn_text in enumerate(line):
                button = QPushButton(btn_text)
                button.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                )
                button.setMinimumSize(40, 40)
                button.clicked.connect(
                    lambda _, b=btn_text: self.handle_button_click(b, target_input)
                )
                grid.addWidget(button, row, col)
        return grid

    def handle_button_click(self, text, input_field: QLineEdit):
        if text == "C":
            input_field.clear()
        elif text == "←":
            cursor_pos = input_field.cursorPosition()
            if cursor_pos > 0:
                input_field.setText(
                    input_field.text()[: cursor_pos - 1]
                    + input_field.text()[cursor_pos:]
                )
                input_field.setCursorPosition(cursor_pos - 1)
        elif text == "=":
            self.run_calculator()
        else:
            cursor_pos = input_field.cursorPosition()
            text_before = input_field.text()[:cursor_pos]
            text_after = input_field.text()[cursor_pos:]
            input_field.setText(text_before + text + text_after)
            input_field.setCursorPosition(cursor_pos + len(text))

    def create_calculator_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.calc_input = QLineEdit()
        self.calc_input.setPlaceholderText("Enter expression (e.g., 2 + 3 * 4)")
        self.calc_result = QLabel("Result:")
        self.calc_result.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        layout.addWidget(self.calc_input)
        layout.addLayout(self.create_button_grid(self.calc_input))
        layout.addWidget(self.calc_result)

        # Hook up "=" button in grid
        self.calc_input.returnPressed.connect(self.run_calculator)
        tab.setLayout(layout)
        return tab

    def run_calculator(self):
        expr = self.calc_input.text()
        result = calculate_basic(expr)
        self.calc_result.setText(f"Result: {result}")

    def create_postfix_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.postfix_input = QLineEdit()
        self.postfix_input.setPlaceholderText("e.g., ( 3 + 4 ) * 5")
        self.postfix_output = QTextEdit()
        self.postfix_output.setReadOnly(True)
        self.postfix_output.setPlaceholderText("Postfix expression will appear here")

        convert_btn = QPushButton("Convert to Postfix")
        convert_btn.clicked.connect(self.run_postfix)

        layout.addWidget(self.postfix_input)
        layout.addWidget(convert_btn)
        layout.addWidget(self.postfix_output)
        tab.setLayout(layout)
        return tab

    def run_postfix(self):
        expr = self.postfix_input.text()
        try:
            result = infix_to_postfix(expr)
            self.postfix_output.setText(f"Postfix:\n{result}")
        except Exception as e:
            self.postfix_output.setText(f"Error:\n{str(e)}")

    def create_graphing_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.graph_input = QLineEdit()
        self.graph_input.setPlaceholderText("e.g., sin(x) or x**2 + 3*x")
        self.graph_btn = QPushButton("Plot")
        self.graph_widget = GraphWidget()

        self.graph_btn.clicked.connect(self.graph_plot)

        layout.addWidget(self.graph_input, stretch=1)
        layout.addWidget(self.graph_btn, stretch=5)
        layout.addWidget(self.graph_widget, stretch=1)
        tab.setLayout(layout)
        return tab

    def graph_plot(self):
        expr = self.graph_input.text()
        self.graph_widget.plot_expression(expr)

    def load_light_theme(self):
        return """
        QWidget {
            background-color: #f6f8fa;
            color: #1f2937;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            font-size: 15px;
        }

        QLineEdit, QTextEdit {
            background-color: #ffffff;
            color: #111827;
            padding: 12px;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            font-size: 16px;
            selection-background-color: #a5d8ff;
        }

        QPushButton {
            background-color: #e2e8f0;
            border: 1px solid #cbd5e1;
            padding: 14px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 16px;
            color: #1f2937;
            transition: all 0.3s ease;
        }

        QPushButton:hover {
            background-color: #dbeafe;
            color: #1e40af;
        }

        QPushButton:pressed {
            background-color: #bfdbfe;
            border: 1px solid #60a5fa;
            color: #1e3a8a;
        }

        QLabel {
            font-size: 17px;
            font-weight: 500;
            color: #111827;
            padding: 4px;
        }

        QTabWidget::pane {
            border: 1px solid #e5e7eb;
            background-color: #ffffff;
            border-radius: 12px;
            margin-top: 6px;
        }

        QTabBar::tab {
            background: #f1f5f9;
            padding: 10px 16px;
            margin: 4px;
            border-top-left-radius: 14px;
            border-top-right-radius: 14px;
            font-weight: 500;
            color: #374151;
        }

        QTabBar::tab:selected {
            background: #dbeafe;
            color: #1e3a8a;
            font-weight: bold;
        }

        QScrollBar:vertical, QScrollBar:horizontal {
            width: 12px;
            height: 12px;
            background: transparent;
        }

        QScrollBar::handle {
            background: #d1d5db;
            border-radius: 6px;
        }

        QScrollBar::handle:hover {
            background: #9ca3af;
        }

        QToolTip {
            background-color: #fefce8;
            color: #1c1917;
            border: 1px solid #fde68a;
            padding: 6px;
            border-radius: 6px;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
