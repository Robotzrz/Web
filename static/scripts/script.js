let n = 0;
var s = "";
let gift_id = "1";
console.log(b);
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
        s += "000"; 
    }
}

function toggleShip(cell) {
    const currentIndex = parseInt(cell.dataset.index);
    const cells = document.querySelectorAll(".cell");
    if (cell.classList.contains("ship")) {
        cell.classList.remove("ship");
    } else {
        // Проверка на близость кораблей
        if (!isAdjacentToShip(currentIndex, cells)) {
            cell.classList.add("ship");
        } else {
            alert("Нельзя ставить корабли близко друг к другу!");
        }
    }
    let a = gift_id.length;
    // if (a == 1){
    //     s[currentIndex * 3] = "0";
    //     s[currentIndex * 3 + 1] = "0";
    //     s[currentIndex * 3 + 2] = gift_id[0];
    // }
    // else if (a == 2){
    //     s[currentIndex * 3] = "0";
    //     s[currentIndex * 3 + 1] = gift_id[0];
    //     s[currentIndex * 3 + 2] = gift_id[1];
    // }
    // else if (a == 3){
    //     s[currentIndex * 3] = gift_id[0];
    //     s[currentIndex * 3 + 1] = gift_id[1];
    //     s[currentIndex * 3 + 2] = gift_id[2];
    // }
    // else{
    //     s[currentIndex * 3] = "0";
    //     s[currentIndex * 3 + 1] = "0";
    //     s[currentIndex * 3 + 2] = "0";
    // }
    s = s.replace
    console.log(s);
}

function isAdjacentToShip(index, cells) {
    const adjacentIndexes = [
        index - boardWidth - 1, index - boardWidth, index - boardWidth + 1,
        index - 1, index + 1,
        index + boardWidth - 1, index + boardWidth, index + boardWidth + 1
    ];

    for (const adjIndex of adjacentIndexes) {
        if (cells[adjIndex] && cells[adjIndex].classList.contains("ship")) {
            return true;
        }
    }

    return false;
}

let add_btn = document.getElementById("add")

add_btn.addEventListener("click", () => {
    // let new_text = document.querySelector("#item").value; // соxраняем текCT
    // document.querySelector("#item").value = ""; // oчишм пoле
    // document.querySelector("#proverka").value = "";

    let item_list = document.querySelector("#fields"); // соxраняем узел списка

    let new_item = document.createElement("div"); // coздаем запись в спискe
    new_item.setAttribute("class", "field"); // присваиваем записи класc


    let item_text = document.createElement("p"); // создаем текст записи
    // item_text.setAttribute("class", "item"); // присваиваем тексту класс
    item_text.innerHTML = 'размер поля:'; // кладем текст из поля ввода внутрь узла

    let item_text1 = document.createElement("p"); // создаем текст записи
    // item_text.setAttribute("class", "item"); // присваиваем тексту класс
    item_text1.innerHTML = boardWidth +  'x' + boardWidth; // кладем текст из поля ввода внутрь узла

    let item_text2 = document.createElement("p"); // создаем текст записи
    // item_text.setAttribute("class", "item"); // присваиваем тексту класс
    item_text2.innerHTML = 'приз:'; // кладем текст из поля ввода внутрь узла

    let item_btn = document.createElement("button"); // coздаем кнопку удаления
    item_btn.setAttribute("id", "item_btn"); // пpисвaиваем кнопке id
    item_btn.innerHTML = "изменить"; // добавляем текст кнопке

    let item_btn2 = document.createElement("button"); // coздаем кнопку удаления
    item_btn2.setAttribute("id", "item_btn2"); // пpисвaиваем кнопке id
    item_btn2.innerHTML = "удалить"; // добавляем текст кнопке

    new_item.appendChild(item_text); // Собираем нашу структуру
    new_item.appendChild(item_text1);
    new_item.appendChild(item_text2); // Собираем нашу структуру
    new_item.appendChild(item_btn);
    new_item.appendChild(item_btn2);
    item_list.appendChild(new_item);

    document.getElementById("pop_up").style.display = "none"

    item_btn2.addEventListener("click", () => {
        let parent = item_btn2.parentNode;
        parent.parentNode.removeChild(parent);
    });
})