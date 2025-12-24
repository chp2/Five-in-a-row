"""
Omok-Lab: AI-Powered Gomoku Analysis Tool
Main entry point for the application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Omok-Lab")
    app.setApplicationVersion("2.4.0")
    app.setOrganizationName("Omok-Lab Team")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
