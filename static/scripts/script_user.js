document.getElementById("choose").addEventListener("click", () => {
    document.getElementById("pop_up").style.display = "block"
})
document.getElementById("close").addEventListener("click", () => {
    document.getElementById("pop_up").style.display = "none"
})



let n = 0;
var s = "";
let gift_id = "1";
document.getElementById("create").addEventListener("click", () => {
    document.getElementById("pop_up").style.display = "block"
})
document.addEventListener("DOMContentLoaded", function() {
    createBoard();
});

function createBoard() {
    const widthInput = document.getElementById("board-width");

    boardWidth = parseInt(widthInput.value);

    const boardContainer = document.getElementById("board-container");
    boardContainer.style.setProperty('--board-width', boardWidth);
    boardContainer.innerHTML = ""; // Очищаем поле перед созданием нового

    for (let i = 0; i < boardWidth * boardWidth; i++) {
        const cell = document.createElement("div");
        cell.classList.add("cell");
        cell.dataset.index = i;
        boardContainer.appendChild(cell);

        cell.addEventListener("click", function() {
            toggleShip(cell);
        });
    }
}
