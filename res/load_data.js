function parseText(text, nTokensPerRecord, delim = "|") {
    var data = [];
    const lines = text.split("\n");
    for (let i = 0; i < lines.length; i++) {
        const l = lines[i].trim();
        const tokens = l.split(delim);
        if (l.startsWith("#") || tokens.length != nTokensPerRecord)
            continue;
        
        let record = [];
        for (let j = 0; j < tokens.length; j++)
            record.push(tokens[j].trim());
        data.push(record);
    }
    return data;
}

function loadPubs(text) {
    var name = document.getElementById("name").innerText;
    var boldName = "<b>" + name + "</b>";
    var pubs = document.getElementById("pubs");
    pubs.innerHTML = "";
    
    // six fields: authors, title, conf/journal, conf/journal abbr., year, other info.
    var data = parseText(text, 6);

    // in reversed order, i.e., the latest appears first
    for (let i = data.length - 1; i >= 0; i--) {
        const record = data[i];
        let li = document.createElement("li");
        let lineText = record[0].replaceAll(name, boldName) + ", \""
                     + record[1] + "\", " + record[2] + " (<b>" + record[3]
                     + "</b>), " + record[4] + ". " + record[5];
        li.innerHTML = lineText;
        pubs.appendChild(li);
    }
}

function loadAwards(text) {
    var awards = document.getElementById("awards");
    awards.innerHTML = "";
    
    // two fields: award, other info.
    var data = parseText(text, 2);

    for (let i = 0; i < data.length; i++) {
        const record = data[i];
        let li = document.createElement("li");
        let lineText = record[0] + ", " + record[1] + ".";
        li.innerHTML = lineText;
        awards.appendChild(li);
    }
}

function loadTextAndPerform(url, callback_func) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader("Content-Type");
            if (type.indexOf("text") !== 1) {
                callback_func(request.responseText);
                return;
            }
        }
    }
}

function loadAll() {
    loadTextAndPerform("res/pubs.txt", loadPubs);
    loadTextAndPerform("res/awards.txt", loadAwards);
}
