function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}


function validateInput() {
    var usernameInput = document.getElementById("username").value;
    var regex = /^[a-zA-Z0-9\-]+$/; // Autoriser les lettres, les chiffres et le tiret "-"

    if (!regex.test(usernameInput)) {
        alert("Saisie invalide. Veuillez utiliser uniquement des lettres, des chiffres et le tiret.");
        return false;
    }
    return true;
}




function showCategory(categoryId) {
    document.querySelectorAll('.category-content').forEach(element => {
        element.style.display = 'none';
    });
    document.getElementById(categoryId).style.display = 'block';

    // Hide all sub-sections within the category
    if (categoryId === 'motos') {
        document.getElementById('motosAll').style.display = 'none';
        document.getElementById('motosByYear').style.display = 'none';
        document.getElementById('motosByMarque').style.display = 'none';
    } else if(categoryId === 'lieux'){
        document.getElementById('lieuxAll').style.display = 'none'; 
    } else if(categoryId == 'marques'){
        document.getElementById('marquesAll').style.display = 'none';
    } else if(categoryId == 'ventes'){
        document.getElementById('ventesAll').style.display = 'none';
    }
}

function searchByYear() {
    var year = document.getElementById("yearSelect").value;
    fetch('/searchByYear?year=' + year)
        .then(response => response.text())
        .then(data => {
            var resultsTable = "<table><thead><tr><th>Modèle</th><th>Année</th><th>Marque</th><th>Cylindrée en cm³</th><th>Puissance en chevaux</th><th>Immatriculation</th><th>Prix neuf</th></tr></thead><tbody>";
            var motos = data.split('\n'); // Divise les données en lignes
            motos.forEach(moto => {
                var motoInfo = moto.split(','); // Divise chaque ligne en colonnes
                resultsTable += `<tr><td>${motoInfo[0]}</td><td>${motoInfo[1]}</td><td>${motoInfo[2]}</td><td>${motoInfo[3]}</td><td>${motoInfo[4]}</td><td>${motoInfo[5]}</td><td>${motoInfo[6]}</td></tr>`;
            });
            resultsTable += "</tbody></table>";

            var resultsDiv = document.getElementById("yearResults");
            resultsDiv.innerHTML = resultsTable;
        })
        .catch(error => console.error('Error:', error));
}


function searchByMarque() {
    var marque = document.getElementById("marqueSelect").value;
    fetch('/searchByMarque?marque=' + marque)
        .then(response => response.text())
        .then(data => {
            var resultsDiv = document.getElementById("marqueResults");
            if (data.trim() === "") {
                resultsDiv.innerHTML = ""; // Si aucune moto n'est trouvée, effacer le contenu de la div
            } else {
                var resultsTable = "<table><thead><tr><th>Modèle</th><th>Année</th><th>Marque</th><th>Cylindrée en cm³</th><th>Puissance en chevaux</th><th>Immatriculation</th><th>Prix neuf</th></tr></thead><tbody>";
                var motos = data.split('\n'); // Divise les données en lignes
                motos.forEach(moto => {
                    var motoInfo = moto.split(','); // Divise chaque ligne en colonnes
                    resultsTable += `<tr><td>${motoInfo[0]}</td><td>${motoInfo[1]}</td><td>${motoInfo[2]}</td><td>${motoInfo[3]}</td><td>${motoInfo[4]}</td><td>${motoInfo[5]}</td><td>${motoInfo[6]}</td></tr>`;
                });
                resultsTable += "</tbody></table>";
                resultsDiv.innerHTML = resultsTable;
            }
        })
        .catch(error => console.error('Error:', error));
}


function validateForm(category) {
    var inputs = document.querySelectorAll('#' + category + ' input[type="text"]');
    var regex = /^[a-zA-Z0-9\-\ ]+$/; // Autoriser les lettres, les chiffres et le tiret "-"
    
    for (var i = 0; i < inputs.length; i++) {
        var inputValue = inputs[i].value.trim();
        
        // Vérifier si le champ est vide
        if (inputValue === '') {
            if (inputs[i].name === 'nomMagasin') {
                inputs[i].value = 'particulier'; // Remplir le champ nomMagasin avec "particulier" si vide
            } else {
                alert('Veuillez remplir tous les champs.');
                return false;
            }
        } else {
            // Vérifier si le champ contient des caractères non autorisés
            if (!regex.test(inputValue)) {
                alert('Le champ ' + inputs[i].name + ' contient des caractères non autorisés. Veuillez utiliser uniquement des lettres, des chiffres et le tiret.');
                return false;
            }
        }
    }
    return true;
}


function uploadCSV(event, category) {
    event.preventDefault();

    var form = event.target;
    var formData = new FormData(form);
    formData.append('category', category);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload_csv', true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            var messageElement = document.getElementById('message');
            if (xhr.status === 200) {
                messageElement.innerHTML = "<p>" + xhr.responseText + "</p>";
            } else {
                messageElement.innerHTML = "<p>Une erreur s'est produite : " + xhr.statusText + "</p>";
            }
        }
    };

    xhr.send(formData);
}

function displayMotos(category) {
    // Cacher toutes les divs de contenu
    document.getElementById('motosAll').style.display = 'none';
    document.getElementById('motosByYear').style.display = 'none';
    document.getElementById('motosByMarque').style.display = 'none';

    // Afficher la div correspondant à la catégorie sélectionnée
    if (category === 'all') {
        document.getElementById('motosAll').style.display = 'block';
    } else if (category === 'byYear') {
        document.getElementById('motosByYear').style.display = 'block';
    } else if (category === 'byMarque') {
        document.getElementById('motosByMarque').style.display = 'block';
    }
}

function displayMotosByYear() {
    var year = document.getElementById("yearSelect").value;
    fetch(`/getMotosByYear?year=${year}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById("yearResults").innerHTML = data;
        });
}

function displayMotosByMarque() {
    var marque = document.getElementById("marqueSelect").value;
    fetch(`/getMotosByMarque?marque=${marque}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById("marqueResults").innerHTML = data;
        });
}

function showLieux() {
    document.getElementById('lieuxAll').style.display = 'block';
}   

function showMarque() {
    document.getElementById('marquesAll').style.display = 'block';
}  

function showVentes() {
    document.getElementById('ventesAll').style.display = 'block';
}  

function displayVentes(type) {
    fetch(`/ventes?type=${type}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('ventesContent').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function displayMessage(modalId, message) {
    document.getElementById(modalId + "_message").innerHTML = message;
}

// JavaScript pour faire défiler automatiquement le diaporama
let slideIndex = 0;
showSlides();

function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}
    slides[slideIndex-1].style.display = "block";
    setTimeout(showSlides, 3500); // Change l'image toutes les 2 secondes
}
document.addEventListener('keydown', function(event) {
    // Empêcher Ctrl+R (pour recharger la page)
    if (event.ctrlKey && event.key === 'r') {
        event.preventDefault();
        alert('Rechargement de la page désactivé.');
    }

    // Empêcher F5 (pour recharger la page)
    if (event.key === 'F5') {
        event.preventDefault();
        alert('Rechargement de la page désactivé.');
    }
});
window.onclick = function(event) {
    if (event.target.className === "modal") {
        closeModal(event.target.id);
    }
}

window.onload = function() {
    // Cache tous les contenus de catégorie par défaut
    document.querySelectorAll('.category-content').forEach(element => {
        element.style.display = 'none';
    });

    // Vérifie si le fragment de l'URL est "#inscription"
    if (window.location.hash === "#inscription") {
        // Affiche le modal d'inscription
        openModal('signupModal');
    }
    // Vérifie si le fragment de l'URL est "#connexion"
    else if (window.location.hash === "#connexion") {
        // Affiche le modal de connexion
        openModal('loginModal');
    }
};