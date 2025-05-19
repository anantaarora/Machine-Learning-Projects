(function() {
  'use strict';

  var email_flag = 0;
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
          //showValidate(this);
        }

        if (email_flag == 1){
          $(this).removeClass("is-valid");
          $(this).addClass("is-invalid");
          event.preventDefault();
          event.stopPropagation();
          return false;
        }

        form.classList.add('was-validated');

      }, false);
    });
  }, false);


  $(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
  });

  $("#picname").change(function(){
      var allowedFiles = [".jpg", ".jpeg", ".png", ".gif"];
      var fileUpload = document.getElementById("picname");
      var lblError = document.getElementById("lblError1");
      var regex = new RegExp("([a-zA-Z0-9\s_\\.\-:])+(" + allowedFiles.join('|') + ")$");
      if (!regex.test(fileUpload.value.toLowerCase())) {
          lblError.innerHTML = "Please upload files having extensions: <b>" + allowedFiles.join(', ') + "</b> only.";
          //$(".needs-validation").addClass('was-validated');
          $(this).addClass("is-invalid");
          lblError.style.display = "block";
          file_flag = 1;
          return false;
      }
      lblError.innerHTML = "";
      $(this).removeClass("is-invalid");
      $(this).addClass("is-valid");
      file_flag = 0;
      return true;
  });

  var inputs = $('input, select')
                .not(':input[type=file]');

  $(inputs).each(function(){
    $(this).change(function() {
      if ($(this)[0].checkValidity() === false) {
          $(this).addClass("is-invalid");
          return false;
      }

      if($(this).attr('type') == 'email' || $(this).attr('name') == 'email') {
        if($(this).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
            $(this).addClass("is-invalid");
            email_flag = 1;
            return false;
        }
        else{
          email_flag = 0;
        }
      }

      $(this).removeClass("is-invalid");
      $(this).addClass("is-valid");
      return true;
    });
  });

})();
