
// Erreurs ajax
$(document).ajaxError(function (xhr, props) {
    // expiration de session
    if (props.status === 401) {
        location.reload();
    }
});

function isNullOrEmpty(objet) {
    if (objet == null || objet == undefined || objet == '') {
        return true;
    }
    return false;
}
function cursor_wait() {
    document.body.style.cursor = "wait";
}
function cursor_clear() {
    document.body.style.cursor = "default";
}
//Pour rafraichir la page
function refreshPage() {
   window.location.reload(true);
}
function isNullOrEmpty(objet) {
    if (objet == null || objet == undefined || objet == '') {
        return true;
    }
    return false;
}
//Facilite l'affichage des notifications bootstrap avec les éléments json renvoyé par __notifSuccess__, __notifError, etc...
function notify(data) {
    $.notify({
        icon: data.icon,
        message: data.msg
    }, {
        type: data.typeNotif,
        delay: isNullOrEmpty(data.delay) ? 5000 : data.delay
    });
}

var imgSupprimerRenderer = function (instance, td, row, col, prop, value, cellProperties) {
  var $img= $('<img src="/static/images/icon_poubelle.png" width="24" height="24" onclick="supprimer('+value+','+row+')">');
  $(td).empty().append($img);
  $(td).attr('class', 'htCenter');
};
var imgModifierRenderer = function (instance, td, row, col, prop, value, cellProperties) {
  var $img= $('<img src="/static/images/pencil.png" width="20" height="20" onclick="modifier('+value+','+row+')">');
  $(td).empty().append($img);
  $(td).attr('class', 'htCenter');
};


//Copy de l'url webdav sur clique de l icone de fichier au niveau des menus
function copyUrlWebdav() {
    $("#webdavURL").show();
    var copyText = document.querySelector("#webdavURL");
    copyText.select();
    document.execCommand("copy");
    $("#webdavURL").hide();
    alert(" Le chemin d'accès aux fichiers est désormais copié dans le presse-papier.\n\n Vous pouvez maintenant ouvrir un Explorateur de fichiers (Win+E) et coller l'adresse du répertoire.\n Authentification ATLAS en production sinon HERCULE.")
}
// Div gif de chargement...
$(document).ready(function () {
    var loading = $('#loadingDiv').hide();
    $(document)
      .ajaxStart(function () {
          loading.show();
      })
      .ajaxStop(function () {
          loading.hide();
      });
});



