// Получаем элементы модального окна и изображения
const modal = document.getElementById("modal");
const modalImage = document.getElementById("modal-image");

// Отображаем модальное окно и устанавливаем источник изображения
function displayModal(obj)
{
    style = obj.currentStyle || window.getComputedStyle(obj, false),
    bi = style.backgroundImage.slice(4, -1).replace(/"/g, "");
    modal.style.display = "block";
    modalImage.src = bi;
}

// Скрываем содержимое модального окна, если пользователь кликнул вне его
function hideModal()
{  
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

