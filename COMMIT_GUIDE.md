# Git Commit Guide for Omok-Lab

## 📋 Summary of Changes

This commit includes the complete implementation of **Omok-Lab v2.4.0**, an AI-powered Gomoku analysis tool.

### New Files Added:

#### Documentation
- `PRD.md` - Complete Product Requirements Document

#### Core Engine (`core/`)
- `core/__init__.py` - Module initialization
- `core/board.py` - Board state management with 15x15 grid
- `core/rule_engine.py` - Renju rule enforcement (3-3, 4-4, overline)
- `core/evaluator.py` - Position evaluation and win probability
- `core/minimax.py` - AI algorithm with Alpha-Beta pruning

#### User Interface (`ui/`)
- `ui/__init__.py` - UI module initialization
- `ui/board_widget.py` - Game board rendering with PyQt6
- `ui/sidebar_widget.py` - Analysis panel with charts and history
- `ui/main_window.py` - Main application window

#### Application
- `main.py` - Application entry point (updated)

#### Assets
- `assets/` - Directory for future assets

### Modified Files:
- `requirements.txt` - Updated with PyQt6, PyQt6-Charts, numpy

---

## 🚀 How to Commit and Push

### Option 1: Using GitHub Desktop (Recommended if you have it)

1. Open **GitHub Desktop**
2. It should automatically detect the changes in `C:\Five-in-a-row`
3. Review all the changed files in the left panel
4. Write a commit message:
   ```
   feat: Implement Omok-Lab v2.4.0 - AI-powered Gomoku game
   
   - Add complete MVC architecture with core game engine
   - Implement Renju rule enforcement (3-3, 4-4, overline)
   - Add Minimax AI with Alpha-Beta pruning
   - Create PyQt6 UI with board, sidebar, and analysis features
   - Add player selection dialog and real-time AI analysis
   - Include win probability chart and move history
   - Add comprehensive PRD documentation
   ```
5. Click **"Commit to main"** (or your branch name)
6. Click **"Push origin"** to push to GitHub

---

### Option 2: Using Git Command Line

If you have Git installed, open **PowerShell** or **Command Prompt** and run:

```bash
# Navigate to the project directory
cd C:\Five-in-a-row

# Check current status
git status

# Add all new and modified files
git add .

# Commit with a descriptive message
git commit -m "feat: Implement Omok-Lab v2.4.0 - AI-powered Gomoku game

- Add complete MVC architecture with core game engine
- Implement Renju rule enforcement (3-3, 4-4, overline)
- Add Minimax AI with Alpha-Beta pruning
- Create PyQt6 UI with board, sidebar, and analysis features
- Add player selection dialog and real-time AI analysis
- Include win probability chart and move history
- Add comprehensive PRD documentation"

# Push to remote repository
git push origin main
```

**Note:** Replace `main` with your branch name if different (e.g., `master`)

---

### Option 3: Install Git First

If Git is not installed:

1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal/IDE
4. Follow **Option 2** above

---

## 📝 Detailed Commit Message Template

If you want to be more detailed, use this template:

```
feat: Implement Omok-Lab v2.4.0 - AI-powered Gomoku analysis tool

## Features Implemented

### Core Game Engine
- 15x15 board management with move history
- Complete Renju rule enforcement
  - 3-3 (double three) detection for black
  - 4-4 (double four) detection for black
  - Overline (6+ stones) detection for black
- Win condition detection (exactly 5 for black, 5+ for white)

### AI System
- Minimax algorithm with Alpha-Beta pruning
- Position evaluation with pattern recognition
- Win probability calculation
- Asynchronous AI computation (no UI blocking)
- Strategic move analysis in English

### User Interface
- PyQt6-based desktop application
- Beautiful wood-textured game board
- Real-time forbidden move indicators (red X)
- AI move recommendations (green pulsing circle)
- Win probability chart with live updates
- Move history table with coordinate notation
- AI chat interface with natural language explanations
- Player color selection dialog at game start
- Dark theme matching design mockup

### Documentation
- Complete Product Requirements Document (PRD)
- Updated README with project description
- Requirements file with all dependencies

## Technical Details
- Architecture: MVC pattern
- Language: Python 3.10+
- GUI Framework: PyQt6
- Dependencies: numpy, PyQt6, PyQt6-Charts

## Testing
- Application runs successfully
- Player selection dialog works
- AI makes strategic moves
- Forbidden moves are correctly detected
- Win conditions are properly handled
```

---

## 🔍 Files to Review Before Committing

Make sure these files are included:

- [x] `PRD.md`
- [x] `main.py`
- [x] `requirements.txt`
- [x] `core/__init__.py`
- [x] `core/board.py`
- [x] `core/rule_engine.py`
- [x] `core/evaluator.py`
- [x] `core/minimax.py`
- [x] `ui/__init__.py`
- [x] `ui/board_widget.py`
- [x] `ui/sidebar_widget.py`
- [x] `ui/main_window.py`

---

## ⚠️ Important Notes

1. **Don't commit** the old `fiverow_sample.py` if you want to keep the repo clean (you can delete it or add to `.gitignore`)
2. **Check** if there are any `__pycache__` directories - these should be in `.gitignore`
3. **Verify** the application runs before pushing
4. **Test** on a clean environment if possible

---

## 🎯 After Pushing

1. Visit your GitHub repository
2. Verify all files are uploaded
3. Check that the README displays correctly
4. Consider adding:
   - Screenshots of the running application
   - GIF demo of gameplay
   - Installation instructions
   - Contributing guidelines

---

## 📞 Need Help?

If you encounter any issues:
1. Check Git installation: `git --version`
2. Check remote URL: `git remote -v`
3. Verify you're on the correct branch: `git branch`
4. Make sure you have push permissions to the repository

Good luck! 🚀
