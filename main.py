import sys
import math
import re
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QGridLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AdvancedCalculator(QWidget):
    """
    Scientific and Basic Mobile Calculator built with PyQt6.
    Includes dynamic panel toggling, expression formatting, and keyboard support.
    """
    def __init__(self):
        super().__init__()
        self.expression = ""
        self.is_expanded = False
        self.is_new_calculation = False
        self.init_ui()

    def init_ui(self):
        """Initializes the window layout, displays, and button grids."""
        self.setObjectName("main_window")
        self.setWindowTitle("Mobile Calculator")
        self.setFixedSize(320, 530)

        # Enable window transparency for compositors like Hyprland/Sway
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(12)

        # Output displays (History label on top, primary result display below)
        self.lbl_history = QLabel("")
        self.lbl_history.setObjectName("lbl_history")
        self.lbl_history.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.lbl_result = QLabel("0")
        self.lbl_result.setObjectName("lbl_result")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(self.lbl_history)
        main_layout.addWidget(self.lbl_result)

        # Horizontal body layout holding optional scientific and main panels side-by-side
        self.body_layout = QHBoxLayout()
        self.body_layout.setSpacing(12)

        # Scientific Panel (2 columns x 5 rows grid)
        self.sci_widget = QWidget()
        grid_sci = QGridLayout(self.sci_widget)
        grid_sci.setContentsMargins(0, 0, 0, 0)
        grid_sci.setSpacing(10)

        sci_buttons = [
            ('sin', 0, 0), ('cos', 0, 1),
            ('tan', 1, 0), ('log', 1, 1),
            ('ln', 2, 0),  ('√', 2, 1),
            ('x²', 3, 0),  ('π', 3, 1),
            ('(', 4, 0),   (')', 4, 1)
        ]

        for text, row, col in sci_buttons:
            btn = QPushButton(text)
            btn.setProperty("class", "sci")
            btn.setFixedSize(60, 60)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(self.on_button_click)
            grid_sci.addWidget(btn, row, col)

        self.sci_widget.setVisible(False)
        self.body_layout.addWidget(self.sci_widget)

        # Basic Panel (4 columns x 5 rows grid)
        basic_widget = QWidget()
        grid_basic = QGridLayout(basic_widget)
        grid_basic.setContentsMargins(0, 0, 0, 0)
        grid_basic.setSpacing(10)

        basic_buttons = [
            ('AC', 0, 0, 'top'), ('⟵', 0, 1, 'top'), ('%', 0, 2, 'top'), ('÷', 0, 3, 'op'),
            ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('×', 1, 3, 'op'),
            ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
            ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
            ('f(x)', 4, 0, 'expand'), ('0', 4, 1, 'num'), ('.', 4, 2, 'num'), ('=', 4, 3, 'op')
        ]

        for text, row, col, btn_type in basic_buttons:
            btn = QPushButton(text)
            btn.setFixedSize(60, 60)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            if text == 'AC':
                self.btn_ac = btn
                btn.setProperty("class", "top")
            elif btn_type == 'expand':
                btn.setObjectName("btn_expand")
            else:
                btn.setProperty("class", btn_type)

            btn.clicked.connect(self.on_button_click)
            grid_basic.addWidget(btn, row, col)

        self.body_layout.addWidget(basic_widget)
        main_layout.addLayout(self.body_layout)
        self.setLayout(main_layout)

    def format_expression(self, expr):
        """
        Formats raw math expressions by adding comma thousands separators to numbers.
        
        Example:
            Input:  "1234567.89+5000"
            Output: "1,234,567.89+5,000"
        """
        if not expr:
            return "0"
        
        def format_number(match):
            num_str = match.group(0)
            if '.' in num_str:
                integers, decimals = num_str.split('.', 1)
                integers_formatted = f"{int(integers):,}" if integers else "0"
                return f"{integers_formatted}.{decimals}"
            else:
                return f"{int(num_str):,}"

        return re.sub(r'\b\d+(\.\d+)?\b', format_number, expr)

    def update_ac_button(self):
        """Toggles the 'AC' (All Clear) button label between 'C' and 'AC' based on input state."""
        if self.expression:
            self.btn_ac.setText("C")
        else:
            self.btn_ac.setText("AC")

    def toggle_expansion(self):
        """Toggles the scientific panel visibility and expands/shrinks the window width accordingly."""
        self.is_expanded = not self.is_expanded
        self.sci_widget.setVisible(self.is_expanded)
        self.setFixedSize(460 if self.is_expanded else 320, 530)

    def process_action(self, action):
        """
        Main handler for calculation logic, string replacement, and error catching.
        
        Examples:
            - Pressing 'sin': Appends "sin(" to expression string.
            - Pressing '=': Converts operators (e.g. '÷' -> '/'), balances parentheses,
                            evaluates expression via math module, and formats result display.
        """
        if self.is_new_calculation:
            if action in ('+', '-', '×', '÷', '%', 'x²'):
                self.lbl_history.setText(self.format_expression(self.expression))
                self.is_new_calculation = False
            elif action not in ('=', 'f(x)'):
                self.lbl_history.setText(self.format_expression(self.expression))
                self.expression = ""
                self.lbl_result.setText("0")
                self.is_new_calculation = False

        if action in ('AC', 'C'):
            self.expression = ""
            self.lbl_history.setText("")
            self.lbl_result.setText("0")
            self.is_new_calculation = False

        elif action in ('⟵', '⌫'):
            self.expression = self.expression[:-1]
            self.lbl_result.setText(self.format_expression(self.expression))

        elif action == 'f(x)':
            self.toggle_expansion()
            return

        elif action == '=':
            if not self.expression:
                return

            try:
                expr_eval = self.expression

                # Automatically close missing unclosed parentheses
                open_parentheses = expr_eval.count('(')
                close_parentheses = expr_eval.count(')')
                if open_parentheses > close_parentheses:
                    expr_eval += ')' * (open_parentheses - close_parentheses)
                    self.expression = expr_eval

                # Map visual operators to Python evaluate-compatible math functions
                expr_eval = (expr_eval
                             .replace('÷', '/').replace('×', '*').replace('%', '/100')
                             .replace('π', 'math.pi').replace('√', 'math.sqrt')
                             .replace('sin', 'math.sin').replace('cos', 'math.cos')
                             .replace('tan', 'math.tan').replace('log', 'math.log10')
                             .replace('ln', 'math.log').replace('x²', '**2'))
                
                result = eval(expr_eval)
                
                self.lbl_history.setText(self.format_expression(self.expression))
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                if isinstance(result, float):
                    self.lbl_result.setText(f"{result:,.4f}".rstrip('0').rstrip('.'))
                else:
                    self.lbl_result.setText(f"{result:,}")
                
                self.expression = str(result)
                self.is_new_calculation = True

            except Exception:
                self.lbl_result.setText("Error")
                self.expression = ""
                self.is_new_calculation = False

        else:
            if action in ('sin', 'cos', 'tan', 'log', 'ln', '√'):
                self.expression += f"{action}("
            elif action == 'x²':
                self.expression += "²"
            else:
                self.expression += action
            
            self.lbl_result.setText(self.format_expression(self.expression))

        self.update_ac_button()

    def on_button_click(self):
        """Signal callback triggered whenever any GUI button is clicked."""
        button = self.sender()
        self.process_action(button.text())

    def keyPressEvent(self, event):
        """
        Handles physical keyboard inputs and maps keys to calculator actions.
        
        Example Key Mappings:
            - Enter/Return -> '='
            - Backspace    -> '⟵'
            - Escape       -> 'AC'
            - '*' or 'x'   -> '×'
        """
        key = event.key()
        text = event.text()

        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            self.process_action(text)
        elif key in (Qt.Key.Key_Plus, Qt.Key.Key_Minus):
            self.process_action(text)
        elif key in (Qt.Key.Key_Asterisk, Qt.Key.Key_X):
            self.process_action('×')
        elif key == Qt.Key.Key_Slash:
            self.process_action('÷')
        elif key == Qt.Key.Key_Percent:
            self.process_action('%')
        elif key in (Qt.Key.Key_Period, Qt.Key.Key_Comma):
            self.process_action('.')
        elif key == Qt.Key.Key_Backspace:
            self.process_action('⟵')
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.process_action('=')
        elif key == Qt.Key.Key_Escape:
            self.process_action('AC')
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setDesktopFileName("calculator")
    
    try:
        with open("styles.css", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    calc = AdvancedCalculator()
    calc.show()
    sys.exit(app.exec())