let bird = document.getElementById('bird');
let scoreElement = document.getElementById('score');
let gravity = 1;  // Slowed down gravity
let birdVelocity = 0;
let isGameRunning = true;
let score = 0;
let obstacles = [];
const obstacleSpeed = 5;
const obstacleFrequency = 2000;

// Keydown event to make the bird flap
document.addEventListener('keydown', () => {
    if (isGameRunning) {
        birdVelocity = -10;
    }
});

// Create obstacles dynamically
function createObstacle() {
    let obstacle = document.createElement('div');
    obstacle.classList.add('obstacle');
    obstacle.style.height = Math.random() * (window.innerHeight / 2) + 'px';
    obstacle.style.right = '-100px';
    obstacle.style.top = '0';
    document.getElementById('game-container').appendChild(obstacle);
    obstacles.push(obstacle);
}

// Move obstacles and check collisions
function updateObstacles() {
    obstacles.forEach((obstacle, index) => {
        let obstacleLeft = obstacle.offsetLeft;
        obstacle.style.left = (obstacleLeft - obstacleSpeed) + 'px';

        // Remove obstacles that are off-screen
        if (obstacleLeft < -100) {
            obstacle.remove();
            obstacles.splice(index, 1);
            score++;
            scoreElement.textContent = 'Score: ' + score;
        }

        // Check collisions
        if (
            bird.offsetTop < obstacle.offsetHeight &&
            bird.offsetLeft + bird.offsetWidth > obstacle.offsetLeft &&
            bird.offsetLeft < obstacle.offsetLeft + obstacle.offsetWidth
        ) {
            isGameRunning = false;
            alert('Game Over! Your score: ' + score);
            location.reload();
        }
    });
}

// Game loop
function gameLoop() {
    if (isGameRunning) {
        birdVelocity += gravity;
        bird.style.top = (bird.offsetTop + birdVelocity) + 'px';

        // Check for collision with the ground
        if (bird.offsetTop >= window.innerHeight - bird.offsetHeight) {
            isGameRunning = false;
            alert('Game Over! Your score: ' + score);
            location.reload();
        }

        updateObstacles();
    }

    requestAnimationFrame(gameLoop);
}

// Start obstacle creation
setInterval(() => {
    if (isGameRunning) {
        createObstacle();
    }
}, obstacleFrequency);

// Start the game loop
gameLoop();
