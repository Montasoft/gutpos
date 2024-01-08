console.log("desde tienda.js")

function createA(link, text) {
    alert("llegando la función con: ", link, text)
    let a = document.createElement("a");
    if (link) {
        a.setAttribute("href", link);
    }
    if (text) {
        let aText = document.createTextNode(text);
        a.appendChild(aText);
    }
    return a;
}