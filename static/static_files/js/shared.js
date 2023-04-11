export function setError(field, tableErrors, idError, idInput){
    for(let key in tableErrors){
      if(key == field){
        idError.html(tableErrors[key]);
        idInput?.addClass("is-invalid")
      }
      if(tableErrors.hasOwnProperty(field) == false){
        idInput?.addClass("is-valid")
        idInput?.removeClass("is-invalid")
        idError.html(' ')
      }
    }
}

export function removeError(idInputError, idInput){
    idInput?.removeClass("is-invalid")
    idInputError.html(' ')
}


export function toastAlert(icon, message){
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.addEventListener('mouseenter', Swal.stopTimer)
          toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
      })
      
      Toast.fire({
        icon: icon,
        title: message
      })
}

export function swalAlert(icon, title, message){
  Swal.fire({
    icon: icon,
    title: title,
    text: message,
  }).then(function(){ 
    // location.reload();
    }
 );
}


export function swalLikeToast(icon, message){
  Swal.fire({
    position: 'top-end',
    icon: icon,
    title: message,
    showConfirmButton: false,
    timer: 4000
  })
}

export function swalDelete(icon, title, actionToDo, message){
  Swal.fire({
    title: title,
    // text: "You won't be able to revert this!",
    icon: icon,
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Oui supprimer !',
    cancelButtonText: 'Annuler'
  }).then((result) => {
    if (result.isConfirmed) {
      actionToDo
      Swal.fire(
        'Supprimer!',
        message,
        'success'
      )
    }
  })
}


// function to make space after 3 numbers
export function spaceNumber(number){
  var value = (number).toLocaleString(
      undefined, // leave undefined to use the visitor's browser 
                 // locale or a string like 'en-US' to override it.
      { minimumFractionDigits: 0 }
    );
    return value;
}