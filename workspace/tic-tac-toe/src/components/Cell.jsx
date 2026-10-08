import React from 'react';
import '../styles/board.css';

function Cell({ value, onClick }) {
    return (
        <div className="cell" onClick={onClick}>
            {value}
        </div>
    );
}

export default Cell;
