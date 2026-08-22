# 📱 Mobile Calculator (PyQt6)

A sleek, modern, mobile-inspired scientific calculator built with Python and PyQt6. Designed with a custom translucent UI that integrates seamlessly with Linux window compositors (like **Hyprland**, **Sway**, or **Wayland** in general) as well as **Windows**.

---

## ✨ Features

- **Fully Customizable via CSS:** Everything in the app's design (colors, fonts, borders, roundings, glowing effects) can be customized by simply editing the `styles.css` file.
- **Native Translucency:** Uses PySide/PyQt `WA_TranslucentBackground` so your window manager compositor (e.g., Hyprland) can render custom acrylic or blurry transparent backgrounds behind it.
- **Expandable Scientific Panel:** Click the `f(x)` button to dynamically toggle trigonometry (`sin`, `cos`, `tan`), logarithms (`log`, `ln`), powers (`x²`), and square roots (`√`).
- **Smart Formatting:** Automatic comma thousands separators (e.g., `1,234,567.89`) and auto-closing missing parentheses on evaluation.
- **Full Keyboard Support:** Direct mapping for Numpad, Enter (`=`), Backspace (`⟵`), Escape (`AC`), and standard mathematical operators.

---

## 🛠️ Customization (CSS)

You can completely redefine the look and feel of the calculator without modifying any Python code. Just open `styles.css` and change the properties:

- **Window Translucency / Color:** Edit `QWidget#main_window`
- **Button Colors & Borders:** Edit `QPushButton[class="num"]`, `QPushButton[class="op"]`, or `QPushButton[class="sci"]`
- **Typography:** Change fonts and font sizes across displays and buttons.

---

## 📋 Requirements

- Python 3.10+
- PyQt6

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tu-usuario/mobile-calculator.git](https://github.com/tu-usuario/mobile-calculator.git)
   cd mobile-calculator




pip install -r requirements.txt



python main.py



This project is open-source under the MIT License.
