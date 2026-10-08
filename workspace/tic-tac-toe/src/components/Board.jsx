import React, { useState } from 'react';
import Cell from './Cell';
import '../styles/board.css';

function Board() {
    const [cells, setCells] = useState(Array(9).fill(null));
    const [isXTurn, setIsXTurn] = useState(true);

    const handleClick = (index) => {
        if (cells[index] || checkWinner(cells)) {
            return;
        }

        const newCells = [...cells];
        newCells[index] = isXTurn ? 'X' : 'O';
        setCells(newCells);
        setIsXTurn(!isXTurn);
    };

    const checkWinner = (cells) => {
        const winningCombinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ];

        for (let combination of winningCombinations) {
            const [a, b, c] = combination;
            if (cells[a] && cells[a] === cells[b] && cells[a] === cells[c]) {
                return cells[a];
            }
        }
        return null;
    };

    const winner = checkWinner(cells);

    return (
        <div className="board">
            {winner ? (
                <h2>Winner: {winner}</h2>
            ) : (
                <h2>Current Turn: {isXTurn ? 'X' : 'O'}</h2>
            )}
            <div className="grid">
                {cells.map((cell, index) => (
                    <Cell key={index} value={cell} onClick={() => handleClick(index)} />
                ))}
            </div>
        </div>
    );
}

export default Board;
