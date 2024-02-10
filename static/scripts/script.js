let n = 0;
var s = [];
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
        s.push("000"); 
    }
}

function toggleShip(cell) {
    const currentIndex = parseInt(cell.dataset.index);
    const cells = document.querySelectorAll(".cell");
    if (cell.classList.contains("ship")) {
        document.getElementById("pop_up2").style.display = "grid";
        document.getElementById("delete").addEventListener("click", () => {
            cell.classList.remove("ship");
            document.getElementById("pop_up2").style.display = "none"
        })
        document.getElementById("cancel").addEventListener("click", () => {
            document.getElementById("pop_up2").style.display = "none"
        })
    } 
    else {
        // Проверка на близость кораблей
        if (!isAdjacentToShip(currentIndex, cells)) {
            document.getElementById("pop_up2").style.display = "grid";
            document.getElementById("accept").addEventListener("click", () => {
                cell.classList.add("ship");
                document.getElementById("pop_up2").style.display = "none"
            })
            document.getElementById("cancel").addEventListener("click", () => {
                document.getElementById("pop_up2").style.display = "none"
            })
        } else {
            alert("Нельзя ставить корабли близко друг к другу!");
        }
    }
    let a = gift_id.length;
    st = "";
    if (a == 1){
        st = "00" + gift_id[0];
    }
    else if (a == 2){
        st = "0" + gift_id[0] + gift_id[1];
    }
    else if (a == 3){
        st = gift_id
    }
    else{
        st = "---";
    }
    s[currentIndex] = st;
    console.log(s);
    let strok = "";
    for (let i = 0; i < s.length; i++)
    {
        strok += s[i];
    }
    document.getElementById("code").value = strok;
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
    // let new_text = document.querySelector("#item").value; // соxраняем текст
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
function createBoard2(){
    const widthInput = document.getElementById("board-width");

    boardWidth = iz_bazu_dannuh

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
        let s = [999];
        if(s[i] != '---'){
            cell.classList.add("ship");
        }
    }
}