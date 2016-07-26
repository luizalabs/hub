function Editor(input, preview) {
    this.update = function () {
      preview.innerHTML = markdown.toHTML(input.value);
    };
    input.editor = this;
    this.update();
}

function mail_fields() {
    $('#id_email_recipients').parents('.form-group').toggle();
    $('#id_email_subject').parents('.form-group').toggle();
}

$(function () {

    var descriptionTextArea = document.getElementById("id_description"),
        previewContainer = document.getElementById("preview");
    var changeLogPreview = new Editor(descriptionTextArea, previewContainer);

    var changeLog = {
        init: function() {
            $('#btn-preview').on('click', function() {
               changeLogPreview.update();
            });
        }
    }
    changeLog.init();

    // hide mail fields
    mail_fields();

    $('#id_send_mail').change(function () {
      // toggle mail fields
      mail_fields();
    });

});
