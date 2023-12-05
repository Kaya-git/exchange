export function prepareData(details) {
    if (!details) {
        return false;
    }
    let formBody = [];
    for (const property in details) {
        // if (details[property] instanceof File) {
        //     // Если свойство является файлом, добавляем его к формируемому телу запроса
        //     formBody.push(details[property]);
        // } else {
            const encodedKey = encodeURIComponent(property);
            const encodedValue = encodeURIComponent(details[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        // }
    }
    return formBody.join("&");
}

export function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));

    if (cookieValue) {
        return cookieValue.split('=')[1];
    } else {
        return null;
    }
}