# 🌐 Omok-Lab Web Version

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Canvas](https://img.shields.io/badge/Canvas-API-orange?style=flat-square)

> **"오목의 신의 한 수를 찾아서"** - Now playable in your browser!

A stunning web-based version of Omok-Lab, featuring AI-powered Gomoku with Renju rules. Play directly in your browser with no installation required!

---

## ✨ Features

### 🎮 **Full Game Implementation**
- **15x15 Gomoku Board** with beautiful wooden texture
- **Renju Rules Engine** - Detects 3-3, 4-4, and overline forbidden moves
- **Player vs AI** gameplay with adjustable difficulty
- **Move History** tracking with coordinate notation
- **Undo/Redo** functionality

### 🤖 **AI Analysis**
- **Minimax Algorithm** with Alpha-Beta pruning
- **Adjustable Difficulty** (Depth 1-4)
- **Position Evaluation** with real-time scoring
- **AI Hints** - Get suggestions for your next move
- **Performance Metrics** - See nodes evaluated and calculation time

### 🎨 **Premium Design**
- **Dark Mode** with glassmorphism effects
- **Smooth Animations** and micro-interactions
- **Responsive Layout** - Works on desktop and tablet
- **Modern Typography** using Inter font
- **Visual Feedback** for forbidden moves and winning lines

---

## 🚀 Quick Start

### Option 1: Open Locally

1. **Clone or download** this repository
2. **Navigate** to the `web` folder
3. **Open** `index.html` in your browser

That's it! No build process, no dependencies, no installation required.

### Option 2: Deploy to GitHub Pages

1. **Push** the `web` folder to your GitHub repository
2. **Go to** Settings → Pages
3. **Select** the branch and `/web` folder
4. **Save** and wait for deployment

Your game will be live at: `https://[username].github.io/[repo-name]/`

---

## 📁 File Structure

```
web/
├── index.html          # Main HTML structure
├── styles.css          # Premium dark mode styles
├── game.js            # Complete game logic
└── README.md          # This file
```

---

## 🎯 How to Play

### Basic Rules

1. **Black plays first** on any intersection
2. **Players alternate** placing stones
3. **Win by creating** exactly 5 in a row (Black) or 5+ in a row (White)
4. **Black cannot** create forbidden patterns (3-3, 4-4, overline)

### Renju Forbidden Moves (Black Only)

- **3-3**: Cannot create two open threes simultaneously
- **4-4**: Cannot create two open fours simultaneously  
- **Overline**: Cannot create 6 or more in a row

### Controls

- **Click** on the board to place a stone
- **New Game** - Start a fresh game
- **Undo Move** - Take back the last move
- **Get Hint** - AI suggests the best move
- **AI Move** - Let AI make a move for current player

### Settings

- **AI Difficulty**: Adjust search depth (1-4)
- **Show Forbidden Moves**: Display red X marks on forbidden positions
- **Show Coordinates**: Display board coordinates (A-O, 1-15)

---

## 🛠️ Technical Details

### Architecture

The web version follows the same **MVC pattern** as the Python version:

- **Model** (`Board`, `RenjuRuleEngine`, `PositionEvaluator`)
  - Pure game logic with no UI dependencies
  - Manages board state, move validation, and rule enforcement

- **View** (`GameRenderer`)
  - HTML5 Canvas rendering
  - Visual feedback and animations

- **Controller** (`GameController`)
  - User input handling
  - AI integration
  - UI updates

### AI Implementation

```javascript
class MinimaxAI {
    - Minimax algorithm with Alpha-Beta pruning
    - Adjustable search depth (1-4 levels)
    - Position evaluation heuristics
    - Move ordering for better pruning
    - Time limit protection (5 seconds)
}
```

### Performance

- **Depth 1**: ~100 nodes, <50ms
- **Depth 2**: ~1,000 nodes, ~200ms
- **Depth 3**: ~10,000 nodes, ~1-2s
- **Depth 4**: ~50,000 nodes, ~5s

---

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 90+     | ✅ Fully Supported |
| Firefox | 88+     | ✅ Fully Supported |
| Safari  | 14+     | ✅ Fully Supported |
| Edge    | 90+     | ✅ Fully Supported |

**Requirements:**
- HTML5 Canvas support
- ES6+ JavaScript
- CSS Grid & Flexbox

---

## 📝 Deployment Guide

### GitHub Pages (Recommended)

1. **Create a new repository** or use existing one
2. **Upload the web folder** to your repository
3. **Go to Settings** → Pages
4. **Configure source**:
   - Branch: `main` (or your default branch)
   - Folder: `/web` or `/` (if web files are in root)
5. **Save** and wait ~1 minute for deployment

Your site will be available at:
```
https://[username].github.io/[repository-name]/
```

### Custom Domain (Optional)

1. **Add a CNAME file** in the web folder:
   ```
   yourdomain.com
   ```
2. **Configure DNS** at your domain registrar:
   ```
   Type: CNAME
   Name: www
   Value: [username].github.io
   ```
3. **Enable HTTPS** in GitHub Pages settings

---

## 🎨 Customization

### Change Board Colors

Edit `styles.css`:
```css
:root {
    --board-bg: #d4a574;      /* Board background */
    --board-line: #8b6f47;    /* Grid lines */
    --stone-black: #1a1a1a;   /* Black stones */
    --stone-white: #f5f5f5;   /* White stones */
}
```

### Adjust AI Difficulty

Edit `game.js`:
```javascript
// Change default depth
this.maxDepth = 3;  // 1-4

// Change time limit
this.timeLimit = 5000;  // milliseconds
```

### Modify Board Size

Edit `game.js`:
```javascript
const BOARD_SIZE = 15;  // Standard is 15x15
const CELL_SIZE = 50;   // Adjust for different sizes
```

---

## 🐛 Troubleshooting

### Game doesn't load
- Check browser console for errors
- Ensure all three files (HTML, CSS, JS) are in the same folder
- Try a different browser

### AI is too slow
- Reduce AI difficulty to Depth 1 or 2
- Close other browser tabs
- Try on a faster device

### Canvas is blurry
- Check browser zoom (should be 100%)
- Ensure high-DPI display support is enabled

---

## 📄 License

MIT License - Feel free to use, modify, and distribute!

---

## 🙏 Credits

- **Original Python Version**: Omok-Lab Desktop App
- **Design Inspiration**: Modern web design trends
- **Fonts**: [Inter](https://fonts.google.com/specimen/Inter) by Google Fonts
- **Algorithm**: Minimax with Alpha-Beta Pruning

---

## 🔗 Links

- **Live Demo**: [Your GitHub Pages URL]
- **Source Code**: [Your Repository URL]
- **Desktop Version**: [Link to Python version]
- **Report Issues**: [GitHub Issues]

---

<div align="center">

**Built with ❤️ for Gomoku enthusiasts**

⚫ ⚪ ⚫ ⚪ ⚫

</div>
