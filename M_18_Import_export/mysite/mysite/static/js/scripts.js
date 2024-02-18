const displayInDir = document.getElementById('displayInDir');
const displayOutDir = document.getElementById('displayOutDir');

// Устанавливаем значение по умолчанию при загрузке страницы
//window.onload = function () {
//    displayInDir.value = "/home/lynx/test/vserv/";
//    displayOutDir.value = "/home/lynx/test/mp4/";
//};

function handleInDirSelection(input) {
    const selectedDir = input.files[0].webkitRelativePath.split('/')[0]; // получаем первый файл в выбранной директории
    document.getElementById('displayInDir01').value = selectedDir; // отображаем в строке ввода
    // присваиваем значение переменной workdir (можно использовать для отправки на сервер или дальнейшей обработки)
    const workdir = selectedDir;
    console.log('Выбранная директория:', workdir);

    // Получаем список файлов
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = ''; // очищаем предыдущий список файлов

    for (let i = 0; i < input.files.length; i++) {
        const file = input.files[i];
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        const shortname_file = file.webkitRelativePath.split('/')[1];
        listItem.appendChild(document.createTextNode(shortname_file));
        fileList.appendChild(listItem);
    }
}

function handleOutDirSelection(input) {
    const selectedDir = input.files[0].webkitRelativePath.split('/')[0]; // получаем первый файл в выбранной директории
    document.getElementById('displayOutDir01').value = selectedDir; // отображаем в строке ввода
    // присваиваем значение переменной workdir (можно использовать для отправки на сервер или дальнейшей обработки)
    const outDir = selectedDir;
    console.log('Директория назначения:', outDir);

    // Получаем список файлов
    const fileList = document.getElementById('fileOutList');
    fileList.innerHTML = ''; // очищаем предыдущий список файлов

    for (let i = 0; i < input.files.length; i++) {
        const file = input.files[i];
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        const shortname_file = file.webkitRelativePath.split('/')[1];
        listItem.appendChild(document.createTextNode(shortname_file));
        fileList.appendChild(listItem);
    }
}

function handlePostDirSelection(input) {
    const selectedDir = input.files[0].webkitRelativePath.split('/')[0]; // получаем первый файл в выбранной директории
    document.getElementById('displayPostDir01').value = selectedDir; // отображаем в строке ввода
    // присваиваем значение переменной workdir (можно использовать для отправки на сервер или дальнейшей обработки)
    const outDir = selectedDir;
    console.log('Директория назначения:', outDir);
}

function handleVideoBitrateChange(input) {
    const outputVideoBitrate = document.getElementById('outputVideoBitrate');
    outputVideoBitrate.textContent = input.value; // Обновляем значение битрейта при изменении ползунка
    // Здесь можно выполнить дополнительные действия при изменении битрейта
}

function handleAudioBitrateChange(input) {
    const outputAudioBitrate = document.getElementById('outputAudioBitrate');
    outputAudioBitrate.textContent = input.value; // Обновляем значение битрейта при изменении ползунка
    // Здесь можно выполнить дополнительные действия при изменении битрейта
}

function handleResolutionChange(select) {
    const selectedResolution = select.value;
    // Здесь можно выполнить дополнительные действия при изменении разрешения
    console.log("Выбранное разрешение:", selectedResolution);
}
