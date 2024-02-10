item_text.setAttribute("class", "item"); // присваиваем тексту класс 
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
        let s = []; 
        if(s[i] != '---'){ 
            cell.classList.add("ship"); 
        } 
    } 
}
for(let i = 0; i < kolvo_polzovateley; i++){ 
    let item_list = document.querySelector("#right"); // соxраняем узел списка 
 
    let new_item = document.createElement("div"); // coздаем запись в спискe 
    new_item.setAttribute("class", "field"); // присваиваем записи класc 
 
    let item_text = document.createElement("p"); // создаем текст записи 
    // item_text.setAttribute("class", "item"); // присваиваем тексту класс 
    item_text.innerHTML = polzovatel_name; // кладем текст из поля ввода внутрь узла 
 
    let item_text1 = document.createElement("input"); // создаем текст записи 
    // item_text.setAttribute("class", "item"); // присваиваем тексту класс 
}