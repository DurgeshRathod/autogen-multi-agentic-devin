const grid = document.getElementById('grid');
const startButton = document.getElementById('start-button');
const scoreDisplay = document.getElementById('score-value');
const levelDisplay = document.getElementById('level-value');

const ROWS = 20;
const COLS = 10;

// Initialize grid
function createGrid() {
    for (let i = 0; i < ROWS * COLS; i++) {
        const cell = document.createElement('div');
        grid.appendChild(cell);
    }
}

createGrid();

// Game variables
let score = 0;
let level = 1;
let isGameRunning = false;

// Tetris blocks (shapes)
const tetrominoes = {
    I: [[1, 2, 3, 4]],
    O: [[1, 2, 11, 12]],
    T: [[1, 2, 3, 12]],
    S: [[2, 3, 11, 12]],
    Z: [[1, 2, 12, 13]],
    L: [[1, 2, 3, 13]],
    J: [[1, 2, 3, 11]],
};

let currentTetromino = [];
let currentPosition = 4; // Start position in the grid
let intervalId;

// Start game function
function startGame() {
    if (isGameRunning) return;

    isGameRunning = true;
    score = 0;
    level = 1;
    updateScore();
    updateLevel();
    spawnTetromino();
    intervalId = setInterval(moveDown, 500);
}

function updateScore() {
    scoreDisplay.textContent = score;
}

function updateLevel() {
    levelDisplay.textContent = level;
}

// Spawn a random tetromino
function spawnTetromino() {
    const tetrominoKeys = Object.keys(tetrominoes);
    const randomTetromino =
        tetrominoKeys[Math.floor(Math.random() * tetrominoKeys.length)];
    currentTetromino = tetrominoes[randomTetromino][0];
    currentPosition = 4;
    drawTetromino();
}

// Draw tetromino on the grid
function drawTetromino() {
    clearTetromino();
    currentTetromino.forEach((index) => {
        grid.children[currentPosition + index].style.backgroundColor = '#38bdf8';
    });
}

// Clear tetromino from the grid
function clearTetromino() {
    currentTetromino.forEach((index) => {
        grid.children[currentPosition + index].style.backgroundColor = '';
    });
}

// Move tetromino down
function moveDown() {
    clearTetromino();
    currentPosition += COLS;
    drawTetromino();
}

// Event listener for start button
startButton.addEventListener('click', startGame);