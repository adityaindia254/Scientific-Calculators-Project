import ast

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

allowed = {
    "x": None,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "log": np.log,
    "sqrt": np.sqrt,
    "exp": np.exp,
    "abs": np.abs,
}


class ExpressionTree(ast.NodeVisitor):
    def __init__(self, expr):
        self.code = compile(ast.parse(expr, mode="eval"), "<string>", "eval")

    def evaluate(self, x):
        allowed["x"] = x
        return eval(self.code, {"__builtins__": {}}, allowed)


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

    def plot_expression(self, expr):
        x = np.linspace(-10, 10, 400)
        y = []

        tree = ExpressionTree(expr)
        for val in x:
            try:
                y.append(tree.evaluate(val))
            except:
                y.append(np.nan)

        self.ax.clear()
        self.ax.plot(x, y, label=f"y = {expr}", color="cyan")
        self.ax.grid(True)
        self.ax.axhline(0, color="gray")
        self.ax.axvline(0, color="gray")
        self.ax.legend()
        self.canvas.draw()
