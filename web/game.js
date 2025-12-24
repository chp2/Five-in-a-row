// ==========================================
// OMOK-LAB - Game Logic
// ==========================================

// Constants
const BOARD_SIZE = 15;
const CELL_SIZE = 50;
const STONE_RADIUS = 20;
const BOARD_PADDING = 25;

const Stone = {
    EMPTY: 0,
    BLACK: 1,
    WHITE: 2
};

const DIRECTIONS = [
    [0, 1],   // Horizontal
    [1, 0],   // Vertical
    [1, 1],   // Diagonal \
    [1, -1]   // Diagonal /
];

// ==========================================
// BOARD CLASS
// ==========================================

class Board {
    constructor() {
        this.reset();
    }

    reset() {
        this.grid = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(Stone.EMPTY));
        this.moveHistory = [];
        this.currentPlayer = Stone.BLACK;
        this.winner = null;
        this.gameOver = false;
        this.winningLine = [];
    }

    isValidPosition(row, col) {
        return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
    }

    isEmpty(row, col) {
        return this.isValidPosition(row, col) && this.grid[row][col] === Stone.EMPTY;
    }

    placeStone(row, col, stone) {
        if (!this.isEmpty(row, col) || this.gameOver) {
            return false;
        }

        this.grid[row][col] = stone;
        this.moveHistory.push({ row, col, stone, moveNumber: this.moveHistory.length + 1 });

        // Check for win
        if (this.checkWin(row, col, stone)) {
            this.winner = stone;
            this.gameOver = true;
        }

        // Switch player
        this.currentPlayer = stone === Stone.BLACK ? Stone.WHITE : Stone.BLACK;
        return true;
    }

    undoMove() {
        if (this.moveHistory.length === 0) {
            return false;
        }

        const lastMove = this.moveHistory.pop();
        this.grid[lastMove.row][lastMove.col] = Stone.EMPTY;
        this.currentPlayer = lastMove.stone;
        this.winner = null;
        this.gameOver = false;
        this.winningLine = [];
        return true;
    }

    countConsecutive(row, col, stone, direction) {
        const [dr, dc] = direction;
        let count = 1;

        // Count in positive direction
        let r = row + dr;
        let c = col + dc;
        while (this.isValidPosition(r, c) && this.grid[r][c] === stone) {
            count++;
            r += dr;
            c += dc;
        }

        // Count in negative direction
        r = row - dr;
        c = col - dc;
        while (this.isValidPosition(r, c) && this.grid[r][c] === stone) {
            count++;
            r -= dr;
            c -= dc;
        }

        return count;
    }

    getLineStones(row, col, stone, direction) {
        const [dr, dc] = direction;
        const positions = [[row, col]];

        // Positive direction
        let r = row + dr;
        let c = col + dc;
        while (this.isValidPosition(r, c) && this.grid[r][c] === stone) {
            positions.push([r, c]);
            r += dr;
            c += dc;
        }

        // Negative direction
        r = row - dr;
        c = col - dc;
        while (this.isValidPosition(r, c) && this.grid[r][c] === stone) {
            positions.push([r, c]);
            r -= dr;
            c -= dc;
        }

        return positions;
    }

    checkWin(row, col, stone) {
        for (const direction of DIRECTIONS) {
            const count = this.countConsecutive(row, col, stone, direction);

            // For black, exactly 5 wins. For white, 5 or more wins.
            if (stone === Stone.BLACK) {
                if (count === 5) {
                    this.winningLine = this.getLineStones(row, col, stone, direction);
                    return true;
                }
            } else {
                if (count >= 5) {
                    this.winningLine = this.getLineStones(row, col, stone, direction);
                    return true;
                }
            }
        }
        return false;
    }

    copy() {
        const newBoard = new Board();
        newBoard.grid = this.grid.map(row => [...row]);
        newBoard.moveHistory = [...this.moveHistory];
        newBoard.currentPlayer = this.currentPlayer;
        newBoard.winner = this.winner;
        newBoard.gameOver = this.gameOver;
        newBoard.winningLine = [...this.winningLine];
        return newBoard;
    }
}

// ==========================================
// RENJU RULE ENGINE
// ==========================================

class RenjuRuleEngine {
    constructor(board) {
        this.board = board;
    }

    isForbiddenMove(row, col, stone) {
        if (stone !== Stone.BLACK) {
            return false;
        }

        // Temporarily place the stone
        const original = this.board.grid[row][col];
        this.board.grid[row][col] = stone;

        // Check all forbidden patterns
        const is33 = this.isDoubleThree(row, col);
        const is44 = this.isDoubleFour(row, col);
        const isOverline = this.isOverline(row, col);

        // Restore original state
        this.board.grid[row][col] = original;

        return is33 || is44 || isOverline;
    }

    getAllForbiddenPositions(stone) {
        if (stone !== Stone.BLACK) {
            return new Set();
        }

        const forbidden = new Set();
        for (let row = 0; row < BOARD_SIZE; row++) {
            for (let col = 0; col < BOARD_SIZE; col++) {
                if (this.board.isEmpty(row, col)) {
                    if (this.isForbiddenMove(row, col, stone)) {
                        forbidden.add(`${row},${col}`);
                    }
                }
            }
        }
        return forbidden;
    }

    isOverline(row, col) {
        for (const direction of DIRECTIONS) {
            const count = this.board.countConsecutive(row, col, Stone.BLACK, direction);
            if (count >= 6) {
                return true;
            }
        }
        return false;
    }

    isDoubleThree(row, col) {
        let openThrees = 0;
        for (const direction of DIRECTIONS) {
            if (this.isOpenThree(row, col, direction)) {
                openThrees++;
                if (openThrees >= 2) {
                    return true;
                }
            }
        }
        return false;
    }

    isDoubleFour(row, col) {
        let openFours = 0;
        for (const direction of DIRECTIONS) {
            if (this.isOpenFour(row, col, direction)) {
                openFours++;
                if (openFours >= 2) {
                    return true;
                }
            }
        }
        return false;
    }

    isOpenThree(row, col, direction) {
        const pattern = this.getPattern(row, col, direction, 6);
        const openThreePattern = [0, 1, 1, 1, 0];

        for (let i = 0; i <= pattern.length - 5; i++) {
            const segment = pattern.slice(i, i + 5);
            if (JSON.stringify(segment) === JSON.stringify(openThreePattern)) {
                return true;
            }
        }
        return false;
    }

    isOpenFour(row, col, direction) {
        const pattern = this.getPattern(row, col, direction, 7);
        const openFourPattern = [0, 1, 1, 1, 1, 0];

        for (let i = 0; i <= pattern.length - 6; i++) {
            const segment = pattern.slice(i, i + 6);
            if (JSON.stringify(segment) === JSON.stringify(openFourPattern)) {
                return true;
            }
        }
        return false;
    }

    getPattern(row, col, direction, length) {
        const [dr, dc] = direction;
        const pattern = [];
        const startOffset = -Math.floor(length / 2);

        for (let i = 0; i < length; i++) {
            const r = row + (startOffset + i) * dr;
            const c = col + (startOffset + i) * dc;

            if (!this.board.isValidPosition(r, c)) {
                pattern.push(-1);
            } else {
                pattern.push(this.board.grid[r][c]);
            }
        }
        return pattern;
    }

    getForbiddenReason(row, col, stone) {
        if (stone !== Stone.BLACK) {
            return '';
        }

        const original = this.board.grid[row][col];
        this.board.grid[row][col] = stone;

        const reasons = [];
        if (this.isDoubleThree(row, col)) reasons.push('Double Three (3-3)');
        if (this.isDoubleFour(row, col)) reasons.push('Double Four (4-4)');
        if (this.isOverline(row, col)) reasons.push('Overline (6+ stones)');

        this.board.grid[row][col] = original;
        return reasons.join(', ');
    }
}

// ==========================================
// POSITION EVALUATOR
// ==========================================

class PositionEvaluator {
    constructor(board) {
        this.board = board;
    }

    evaluate(perspective) {
        let score = 0;

        for (let row = 0; row < BOARD_SIZE; row++) {
            for (let col = 0; col < BOARD_SIZE; col++) {
                const stone = this.board.grid[row][col];
                if (stone !== Stone.EMPTY) {
                    const stoneScore = this.evaluatePosition(row, col, stone);
                    score += stone === perspective ? stoneScore : -stoneScore;
                }
            }
        }

        return score;
    }

    evaluatePosition(row, col, stone) {
        let score = 0;

        for (const direction of DIRECTIONS) {
            const count = this.board.countConsecutive(row, col, stone, direction);

            if (count === 5) score += 100000;
            else if (count === 4) score += 10000;
            else if (count === 3) score += 1000;
            else if (count === 2) score += 100;
            else score += 10;
        }

        // Center bonus
        const centerDist = Math.abs(row - 7) + Math.abs(col - 7);
        score += (14 - centerDist) * 5;

        return score;
    }
}

// ==========================================
// MINIMAX AI
// ==========================================

class MinimaxAI {
    constructor(board, maxDepth = 3, timeLimit = 5000) {
        this.board = board;
        this.maxDepth = maxDepth;
        this.timeLimit = timeLimit;
        this.evaluator = new PositionEvaluator(board);
        this.ruleEngine = new RenjuRuleEngine(board);
        this.nodesEvaluated = 0;
        this.startTime = 0;
    }

    getBestMove(stone) {
        this.nodesEvaluated = 0;
        this.startTime = Date.now();

        let bestMove = null;
        let bestScore = -Infinity;
        let alpha = -Infinity;
        let beta = Infinity;

        const candidates = this.getCandidateMoves(stone);

        if (candidates.length === 0) {
            return null;
        }

        for (const [row, col] of candidates) {
            if (Date.now() - this.startTime > this.timeLimit) {
                break;
            }

            if (stone === Stone.BLACK && this.ruleEngine.isForbiddenMove(row, col, stone)) {
                continue;
            }

            this.board.grid[row][col] = stone;
            const score = this.minimax(this.maxDepth - 1, alpha, beta, false, stone);
            this.board.grid[row][col] = Stone.EMPTY;

            if (score > bestScore) {
                bestScore = score;
                bestMove = { row, col, score };
            }

            alpha = Math.max(alpha, score);
        }

        return bestMove;
    }

    minimax(depth, alpha, beta, isMaximizing, perspective) {
        this.nodesEvaluated++;

        if (Date.now() - this.startTime > this.timeLimit) {
            return this.evaluator.evaluate(perspective);
        }

        if (depth === 0 || this.board.gameOver) {
            return this.evaluator.evaluate(perspective);
        }

        const currentStone = isMaximizing ? perspective :
            (perspective === Stone.BLACK ? Stone.WHITE : Stone.BLACK);

        const candidates = this.getCandidateMoves(currentStone, 15);

        if (candidates.length === 0) {
            return this.evaluator.evaluate(perspective);
        }

        if (isMaximizing) {
            let maxEval = -Infinity;
            for (const [row, col] of candidates) {
                if (currentStone === Stone.BLACK && this.ruleEngine.isForbiddenMove(row, col, currentStone)) {
                    continue;
                }

                this.board.grid[row][col] = currentStone;
                const evalScore = this.minimax(depth - 1, alpha, beta, false, perspective);
                this.board.grid[row][col] = Stone.EMPTY;

                maxEval = Math.max(maxEval, evalScore);
                alpha = Math.max(alpha, evalScore);

                if (beta <= alpha) break;
            }
            return maxEval;
        } else {
            let minEval = Infinity;
            for (const [row, col] of candidates) {
                if (currentStone === Stone.BLACK && this.ruleEngine.isForbiddenMove(row, col, currentStone)) {
                    continue;
                }

                this.board.grid[row][col] = currentStone;
                const evalScore = this.minimax(depth - 1, alpha, beta, true, perspective);
                this.board.grid[row][col] = Stone.EMPTY;

                minEval = Math.min(minEval, evalScore);
                beta = Math.min(beta, evalScore);

                if (beta <= alpha) break;
            }
            return minEval;
        }
    }

    getCandidateMoves(stone, limit = 25) {
        const candidates = [];

        if (this.board.moveHistory.length === 0) {
            const center = Math.floor(BOARD_SIZE / 2);
            return [[center, center]];
        }

        for (let row = 0; row < BOARD_SIZE; row++) {
            for (let col = 0; col < BOARD_SIZE; col++) {
                if (this.board.isEmpty(row, col)) {
                    if (this.hasNearbyStone(row, col, 2)) {
                        this.board.grid[row][col] = stone;
                        const score = this.evaluator.evaluate(stone);
                        this.board.grid[row][col] = Stone.EMPTY;
                        candidates.push([row, col, score]);
                    }
                }
            }
        }

        candidates.sort((a, b) => b[2] - a[2]);
        return candidates.slice(0, limit).map(([r, c]) => [r, c]);
    }

    hasNearbyStone(row, col, distance = 2) {
        for (let dr = -distance; dr <= distance; dr++) {
            for (let dc = -distance; dc <= distance; dc++) {
                const r = row + dr;
                const c = col + dc;
                if (this.board.isValidPosition(r, c) && this.board.grid[r][c] !== Stone.EMPTY) {
                    return true;
                }
            }
        }
        return false;
    }
}

// ==========================================
// GAME RENDERER
// ==========================================

class GameRenderer {
    constructor(canvas, board) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.board = board;
        this.ruleEngine = new RenjuRuleEngine(board);
        this.forbiddenPositions = new Set();
        this.hintPosition = null;
        this.lastMove = null;
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawBoard();
        this.drawCoordinates();
        this.drawStones();
        this.drawForbiddenMarks();
        this.drawHint();
        this.drawWinningLine();
    }

    drawBoard() {
        // Board background
        const gradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, this.canvas.height);
        gradient.addColorStop(0, '#d4a574');
        gradient.addColorStop(1, '#c49563');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Grid lines
        this.ctx.strokeStyle = '#8b6f47';
        this.ctx.lineWidth = 1.5;

        for (let i = 0; i < BOARD_SIZE; i++) {
            // Vertical lines
            this.ctx.beginPath();
            this.ctx.moveTo(BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING);
            this.ctx.lineTo(BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE);
            this.ctx.stroke();

            // Horizontal lines
            this.ctx.beginPath();
            this.ctx.moveTo(BOARD_PADDING, BOARD_PADDING + i * CELL_SIZE);
            this.ctx.lineTo(BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE);
            this.ctx.stroke();
        }

        // Star points
        const starPoints = [
            [3, 3], [3, 11], [7, 7], [11, 3], [11, 11]
        ];

        this.ctx.fillStyle = '#6b5635';
        for (const [row, col] of starPoints) {
            const x = BOARD_PADDING + col * CELL_SIZE;
            const y = BOARD_PADDING + row * CELL_SIZE;
            this.ctx.beginPath();
            this.ctx.arc(x, y, 4, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }

    drawCoordinates() {
        if (!document.getElementById('showCoordinates').checked) return;

        this.ctx.fillStyle = '#6b5635';
        this.ctx.font = '12px Inter';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';

        const cols = 'ABCDEFGHJKLMNO';

        // Column labels
        for (let i = 0; i < BOARD_SIZE; i++) {
            const x = BOARD_PADDING + i * CELL_SIZE;
            this.ctx.fillText(cols[i], x, 12);
            this.ctx.fillText(cols[i], x, this.canvas.height - 12);
        }

        // Row labels
        for (let i = 0; i < BOARD_SIZE; i++) {
            const y = BOARD_PADDING + i * CELL_SIZE;
            this.ctx.fillText(String(i + 1), 12, y);
            this.ctx.fillText(String(i + 1), this.canvas.width - 12, y);
        }
    }

    drawStones() {
        for (let row = 0; row < BOARD_SIZE; row++) {
            for (let col = 0; col < BOARD_SIZE; col++) {
                const stone = this.board.grid[row][col];
                if (stone !== Stone.EMPTY) {
                    this.drawStone(row, col, stone);
                }
            }
        }
    }

    drawStone(row, col, stone) {
        const x = BOARD_PADDING + col * CELL_SIZE;
        const y = BOARD_PADDING + row * CELL_SIZE;

        // Shadow
        this.ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        this.ctx.shadowBlur = 8;
        this.ctx.shadowOffsetX = 2;
        this.ctx.shadowOffsetY = 2;

        // Stone
        this.ctx.beginPath();
        this.ctx.arc(x, y, STONE_RADIUS, 0, Math.PI * 2);

        if (stone === Stone.BLACK) {
            const gradient = this.ctx.createRadialGradient(x - 5, y - 5, 0, x, y, STONE_RADIUS);
            gradient.addColorStop(0, '#3a3a3a');
            gradient.addColorStop(1, '#1a1a1a');
            this.ctx.fillStyle = gradient;
        } else {
            const gradient = this.ctx.createRadialGradient(x - 5, y - 5, 0, x, y, STONE_RADIUS);
            gradient.addColorStop(0, '#ffffff');
            gradient.addColorStop(1, '#e5e5e5');
            this.ctx.fillStyle = gradient;
        }

        this.ctx.fill();

        // Reset shadow
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;

        // Highlight last move
        if (this.lastMove && this.lastMove.row === row && this.lastMove.col === col) {
            this.ctx.strokeStyle = '#ef4444';
            this.ctx.lineWidth = 3;
            this.ctx.stroke();
        }

        // Move number
        const move = this.board.moveHistory.find(m => m.row === row && m.col === col);
        if (move) {
            this.ctx.fillStyle = stone === Stone.BLACK ? '#ffffff' : '#000000';
            this.ctx.font = 'bold 12px Inter';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(move.moveNumber, x, y);
        }
    }

    drawForbiddenMarks() {
        if (!document.getElementById('showForbidden').checked) return;

        this.ctx.strokeStyle = '#ef4444';
        this.ctx.lineWidth = 2;

        for (const key of this.forbiddenPositions) {
            const [row, col] = key.split(',').map(Number);
            const x = BOARD_PADDING + col * CELL_SIZE;
            const y = BOARD_PADDING + row * CELL_SIZE;

            // Draw X
            const size = 8;
            this.ctx.beginPath();
            this.ctx.moveTo(x - size, y - size);
            this.ctx.lineTo(x + size, y + size);
            this.ctx.moveTo(x + size, y - size);
            this.ctx.lineTo(x - size, y + size);
            this.ctx.stroke();
        }
    }

    drawHint() {
        if (!this.hintPosition) return;

        const { row, col } = this.hintPosition;
        const x = BOARD_PADDING + col * CELL_SIZE;
        const y = BOARD_PADDING + row * CELL_SIZE;

        // Pulsing circle
        this.ctx.strokeStyle = '#10b981';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.arc(x, y, STONE_RADIUS + 5, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawWinningLine() {
        if (this.board.winningLine.length === 0) return;

        this.ctx.strokeStyle = '#fbbf24';
        this.ctx.lineWidth = 4;
        this.ctx.lineCap = 'round';

        const first = this.board.winningLine[0];
        const last = this.board.winningLine[this.board.winningLine.length - 1];

        const x1 = BOARD_PADDING + first[1] * CELL_SIZE;
        const y1 = BOARD_PADDING + first[0] * CELL_SIZE;
        const x2 = BOARD_PADDING + last[1] * CELL_SIZE;
        const y2 = BOARD_PADDING + last[0] * CELL_SIZE;

        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
    }

    updateForbiddenPositions() {
        this.forbiddenPositions = this.ruleEngine.getAllForbiddenPositions(this.board.currentPlayer);
    }

    getBoardPosition(clientX, clientY) {
        const rect = this.canvas.getBoundingClientRect();
        const x = clientX - rect.left;
        const y = clientY - rect.top;

        const col = Math.round((x - BOARD_PADDING) / CELL_SIZE);
        const row = Math.round((y - BOARD_PADDING) / CELL_SIZE);

        if (row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE) {
            return { row, col };
        }
        return null;
    }
}

// ==========================================
// GAME CONTROLLER
// ==========================================

class GameController {
    constructor() {
        this.board = new Board();
        this.canvas = document.getElementById('gameBoard');
        this.renderer = new GameRenderer(this.canvas, this.board);
        this.ruleEngine = new RenjuRuleEngine(this.board);
        this.ai = null;
        this.isAIThinking = false;

        this.initializeEventListeners();
        this.updateUI();
        this.renderer.draw();
    }

    initializeEventListeners() {
        // Canvas click
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));

        // Buttons
        document.getElementById('newGameBtn').addEventListener('click', () => this.newGame());
        document.getElementById('undoBtn').addEventListener('click', () => this.undoMove());
        document.getElementById('hintBtn').addEventListener('click', () => this.getHint());
        document.getElementById('aiMoveBtn').addEventListener('click', () => this.makeAIMove());

        // Settings
        document.getElementById('aiDifficulty').addEventListener('change', () => this.updateAIDifficulty());
        document.getElementById('showForbidden').addEventListener('change', () => this.renderer.draw());
        document.getElementById('showCoordinates').addEventListener('change', () => this.renderer.draw());
    }

    handleCanvasClick(e) {
        if (this.board.gameOver || this.isAIThinking) return;

        const pos = this.renderer.getBoardPosition(e.clientX, e.clientY);
        if (!pos) return;

        const { row, col } = pos;

        // Check if move is forbidden
        if (this.ruleEngine.isForbiddenMove(row, col, this.board.currentPlayer)) {
            const reason = this.ruleEngine.getForbiddenReason(row, col, this.board.currentPlayer);
            this.showStatus(`Forbidden move: ${reason}`, 'error');
            return;
        }

        // Make move
        if (this.board.placeStone(row, col, this.board.currentPlayer)) {
            this.renderer.lastMove = { row, col };
            this.renderer.hintPosition = null;
            this.updateUI();
            this.renderer.draw();

            // Check for game over
            if (this.board.gameOver) {
                this.handleGameOver();
            }
        }
    }

    newGame() {
        this.board.reset();
        this.renderer.lastMove = null;
        this.renderer.hintPosition = null;
        this.updateUI();
        this.renderer.draw();
        this.showStatus('New game started!', 'success');
    }

    undoMove() {
        if (this.board.undoMove()) {
            this.renderer.lastMove = null;
            this.renderer.hintPosition = null;
            this.updateUI();
            this.renderer.draw();
            this.showStatus('Move undone', 'info');
        }
    }

    async getHint() {
        if (this.board.gameOver || this.isAIThinking) return;

        this.showLoading(true);
        this.isAIThinking = true;

        const depth = parseInt(document.getElementById('aiDifficulty').value);
        this.ai = new MinimaxAI(this.board, depth);

        const startTime = Date.now();

        // Use setTimeout to prevent UI blocking
        setTimeout(() => {
            const bestMove = this.ai.getBestMove(this.board.currentPlayer);
            const calcTime = Date.now() - startTime;

            this.showLoading(false);
            this.isAIThinking = false;

            if (bestMove) {
                this.renderer.hintPosition = { row: bestMove.row, col: bestMove.col };
                this.renderer.draw();

                const cols = 'ABCDEFGHJKLMNO';
                const coord = `${cols[bestMove.col]}${bestMove.row + 1}`;

                document.getElementById('positionScore').textContent = bestMove.score;
                document.getElementById('nodesEvaluated').textContent = this.ai.nodesEvaluated;
                document.getElementById('calcTime').textContent = `${calcTime}ms`;

                const suggestedMoveEl = document.getElementById('suggestedMove');
                suggestedMoveEl.innerHTML = `
                    <strong>Suggested Move:</strong><br>
                    Position: ${coord}<br>
                    Score: ${bestMove.score}
                `;
                suggestedMoveEl.classList.add('active');

                this.showStatus(`AI suggests: ${coord}`, 'success');
            }
        }, 100);
    }

    async makeAIMove() {
        if (this.board.gameOver || this.isAIThinking) return;

        this.showLoading(true);
        this.isAIThinking = true;

        const depth = parseInt(document.getElementById('aiDifficulty').value);
        this.ai = new MinimaxAI(this.board, depth);

        const startTime = Date.now();

        setTimeout(() => {
            const bestMove = this.ai.getBestMove(this.board.currentPlayer);
            const calcTime = Date.now() - startTime;

            this.showLoading(false);
            this.isAIThinking = false;

            if (bestMove) {
                this.board.placeStone(bestMove.row, bestMove.col, this.board.currentPlayer);
                this.renderer.lastMove = { row: bestMove.row, col: bestMove.col };
                this.renderer.hintPosition = null;

                document.getElementById('calcTime').textContent = `${calcTime}ms`;

                this.updateUI();
                this.renderer.draw();

                if (this.board.gameOver) {
                    this.handleGameOver();
                }
            }
        }, 100);
    }

    updateAIDifficulty() {
        const depth = parseInt(document.getElementById('aiDifficulty').value);
        this.showStatus(`AI difficulty set to depth ${depth}`, 'info');
    }

    updateUI() {
        // Current player
        const playerStone = document.getElementById('currentPlayerStone');
        const playerText = document.getElementById('currentPlayerText');

        if (this.board.currentPlayer === Stone.BLACK) {
            playerStone.className = 'stone-indicator black';
            playerText.textContent = 'Black';
        } else {
            playerStone.className = 'stone-indicator white';
            playerText.textContent = 'White';
        }

        // Move number
        document.getElementById('moveNumber').textContent = this.board.moveHistory.length;

        // Move history
        this.updateMoveHistory();

        // Update forbidden positions
        this.renderer.updateForbiddenPositions();

        // Update AI analysis
        this.updateAIAnalysis();
    }

    updateAIAnalysis() {
        // Only update if there are moves on the board
        if (this.board.moveHistory.length === 0) {
            document.getElementById('positionScore').textContent = '0';
            return;
        }

        // Create evaluator to get current position score
        const evaluator = new PositionEvaluator(this.board);

        // Evaluate from current player's perspective
        const score = evaluator.evaluate(this.board.currentPlayer);

        // Update position score
        document.getElementById('positionScore').textContent = score;

        // Add visual indicator based on score
        const scoreEl = document.getElementById('positionScore');
        if (score > 1000) {
            scoreEl.style.color = '#10b981'; // Green for good position
        } else if (score < -1000) {
            scoreEl.style.color = '#ef4444'; // Red for bad position
        } else {
            scoreEl.style.color = '#6366f1'; // Blue for neutral
        }
    }

    updateMoveHistory() {
        const historyEl = document.getElementById('moveHistory');

        if (this.board.moveHistory.length === 0) {
            historyEl.innerHTML = '<div class="empty-state">No moves yet</div>';
            return;
        }

        const cols = 'ABCDEFGHJKLMNO';
        const html = this.board.moveHistory.map(move => {
            const coord = `${cols[move.col]}${move.row + 1}`;
            const stoneClass = move.stone === Stone.BLACK ? 'black' : 'white';
            const stoneName = move.stone === Stone.BLACK ? 'Black' : 'White';

            return `
                <div class="move-item">
                    <span class="move-number">#${move.moveNumber}</span>
                    <span class="move-coord">${coord}</span>
                    <span class="move-player">
                        <span class="move-stone ${stoneClass}"></span>
                        ${stoneName}
                    </span>
                </div>
            `;
        }).reverse().join('');

        historyEl.innerHTML = html;
    }

    handleGameOver() {
        const winner = this.board.winner === Stone.BLACK ? 'Black' : 'White';
        this.showStatus(`🎉 ${winner} wins!`, 'success');

        setTimeout(() => {
            alert(`Game Over!\n\n${winner} wins!`);
        }, 500);
    }

    showStatus(message, type = 'info') {
        const statusEl = document.getElementById('gameStatus');
        const messageEl = statusEl.querySelector('.status-message');

        messageEl.textContent = message;

        // Update color based on type
        if (type === 'error') {
            statusEl.style.background = 'rgba(239, 68, 68, 0.1)';
            statusEl.style.borderLeftColor = '#ef4444';
        } else if (type === 'success') {
            statusEl.style.background = 'rgba(16, 185, 129, 0.1)';
            statusEl.style.borderLeftColor = '#10b981';
        } else {
            statusEl.style.background = 'rgba(99, 102, 241, 0.1)';
            statusEl.style.borderLeftColor = '#6366f1';
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }
}

// ==========================================
// INITIALIZE GAME
// ==========================================

let game;

window.addEventListener('DOMContentLoaded', () => {
    game = new GameController();
});
