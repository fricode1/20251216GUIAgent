class Game2048 {
    constructor() {
        this.gridSize = 4;
        this.cells = [];
        this.score = 0;
        this.bestScore = parseInt(localStorage.getItem('bestScore')) || 0;
        this.over = false;
        this.won = false;
        this.keepPlaying = false;
        
        this.setup();
        this.bindEvents();
        this.startGame();
    }
    
    setup() {
        this.grid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(0));
        this.container = document.querySelector('.tile-container');
        this.scoreDisplay = document.getElementById('score');
        this.bestScoreDisplay = document.getElementById('best-score');
        this.gameMessage = document.querySelector('.game-message');
        this.updateBestScore();
    }
    
    bindEvents() {
        document.addEventListener('keydown', this.handleKeyPress.bind(this));
        document.getElementById('new-game').addEventListener('click', this.restart.bind(this));
        document.querySelector('.retry-button').addEventListener('click', this.restart.bind(this));
        document.querySelector('.keep-playing-button').addEventListener('click', this.keepPlayingFunc.bind(this));
    }
    
    startGame() {
        this.addRandomTile();
        this.addRandomTile();
    }
    
    addRandomTile() {
        if (this.isGridFull()) return;
        
        let value = Math.random() < 0.9 ? 2 : 4;
        let emptyCells = [];
        
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = 0; col < this.gridSize; col++) {
                if (this.grid[row][col] === 0) {
                    emptyCells.push({row, col});
                }
            }
        }
        
        if (emptyCells.length === 0) return;
        
        let cell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        this.grid[cell.row][cell.col] = value;
        this.addTileElement(cell.row, cell.col, value);
    }
    
    addTileElement(row, col, value) {
        let tile = document.createElement('div');
        tile.className = `tile tile-${value} tile-new`;
        tile.textContent = value;
        tile.style.top = this.getPosition(row);
        tile.style.left = this.getPosition(col);
        this.container.appendChild(tile);
    }
    
    getPosition(index) {
        return (index * 121.25) + 'px';
    }
    
    handleKeyPress(event) {
        if (this.over) return;
        
        let moved = false;
        switch(event.key) {
            case 'ArrowUp':
                moved = this.moveUp();
                break;
            case 'ArrowDown':
                moved = this.moveDown();
                break;
            case 'ArrowLeft':
                moved = this.moveLeft();
                break;
            case 'ArrowRight':
                moved = this.moveRight();
                break;
            default:
                return;
        }
        
        if (moved) {
            this.addRandomTile();
            this.updateScore();
            if (this.isGameOver()) {
                this.gameOver();
            }
            if (this.hasWon() && !this.won && !this.keepPlaying) {
                this.won = true;
                this.showMessage('游戏胜利！', true);
            }
        }
    }
    
    moveUp() {
        return this.moveVertical(true);
    }
    
    moveDown() {
        return this.moveVertical(false);
    }
    
    moveLeft() {
        return this.moveHorizontal(true);
    }
    
    moveRight() {
        return this.moveHorizontal(false);
    }
    
    moveVertical(upward) {
        let moved = false;
        
        for (let col = 0; col < this.gridSize; col++) {
            for (let row = upward ? 0 : this.gridSize - 1; 
                 upward ? row < this.gridSize : row >= 0; 
                 upward ? row++ : row--) {
                
                if (this.grid[row][col] !== 0) {
                    let currentRow = row;
                    let targetRow = upward ? row - 1 : row + 1;
                    
                    while (upward ? targetRow >= 0 : targetRow < this.gridSize) {
                        if (this.grid[targetRow][col] === 0) {
                            // 移动到空位置
                            this.grid[targetRow][col] = this.grid[currentRow][col];
                            this.grid[currentRow][col] = 0;
                            currentRow = targetRow;
                            targetRow = upward ? targetRow - 1 : targetRow + 1;
                            moved = true;
                        } else if (this.grid[targetRow][col] === this.grid[currentRow][col]) {
                            // 合并相同数字
                            this.grid[targetRow][col] *= 2;
                            this.grid[currentRow][col] = 0;
                            this.score += this.grid[targetRow][col];
                            moved = true;
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
        }
        
        this.renderTiles();
        return moved;
    }
    
    moveHorizontal(leftward) {
        let moved = false;
        
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = leftward ? 0 : this.gridSize - 1; 
                 leftward ? col < this.gridSize : col >= 0; 
                 leftward ? col++ : col--) {
                
                if (this.grid[row][col] !== 0) {
                    let currentCol = col;
                    let targetCol = leftward ? col - 1 : col + 1;
                    
                    while (leftward ? targetCol >= 0 : targetCol < this.gridSize) {
                        if (this.grid[row][targetCol] === 0) {
                            // 移动到空位置
                            this.grid[row][targetCol] = this.grid[row][currentCol];
                            this.grid[row][currentCol] = 0;
                            currentCol = targetCol;
                            targetCol = leftward ? targetCol - 1 : targetCol + 1;
                            moved = true;
                        } else if (this.grid[row][targetCol] === this.grid[row][currentCol]) {
                            // 合并相同数字
                            this.grid[row][targetCol] *= 2;
                            this.grid[row][currentCol] = 0;
                            this.score += this.grid[row][targetCol];
                            moved = true;
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
        }
        
        this.renderTiles();
        return moved;
    }
    
    clearContainer() {
        this.container.innerHTML = '';
    }
    
    renderTiles() {
        this.clearContainer();
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = 0; col < this.gridSize; col++) {
                if (this.grid[row][col] !== 0) {
                    this.addTileElement(row, col, this.grid[row][col]);
                }
            }
        }
    }
    
    updateScore() {
        this.scoreDisplay.textContent = this.score;
        if (this.score > this.bestScore) {
            this.bestScore = this.score;
            localStorage.setItem('bestScore', this.bestScore);
            this.updateBestScore();
        }
    }
    
    updateBestScore() {
        this.bestScoreDisplay.textContent = this.bestScore;
    }
    
    isGridFull() {
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = 0; col < this.gridSize; col++) {
                if (this.grid[row][col] === 0) {
                    return false;
                }
            }
        }
        return true;
    }
    
    isGameOver() {
        if (!this.isGridFull()) return false;
        
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = 0; col < this.gridSize; col++) {
                let value = this.grid[row][col];
                if (
                    (row > 0 && this.grid[row-1][col] === value) ||
                    (row < this.gridSize-1 && this.grid[row+1][col] === value) ||
                    (col > 0 && this.grid[row][col-1] === value) ||
                    (col < this.gridSize-1 && this.grid[row][col+1] === value)
                ) {
                    return false;
                }
            }
        }
        return true;
    }
    
    hasWon() {
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = 0; col < this.gridSize; col++) {
                if (this.grid[row][col] === 2048) {
                    return true;
                }
            }
        }
        return false;
    }
    
    gameOver() {
        this.over = true;
        this.showMessage('游戏结束！', false);
    }
    
    showMessage(message, isWin) {
        this.gameMessage.querySelector('p').textContent = message;
        this.gameMessage.className = `game-message ${isWin ? 'game-won' : 'game-over'}`;
    }
    
    restart() {
        this.grid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(0));
        this.score = 0;
        this.over = false;
        this.won = false;
        this.keepPlaying = false;
        this.gameMessage.className = 'game-message';
        this.clearContainer();
        this.updateScore();
        this.startGame();
    }
    
    keepPlayingFunc() {
        this.keepPlaying = true;
        this.gameMessage.className = 'game-message';
    }
}

// 启动游戏 - 由HTML文件中的监听器调用
// new Game2048() 调用已在HTML文件中处理