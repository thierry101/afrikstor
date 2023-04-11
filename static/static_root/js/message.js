import {setError, swalAlert, removeError} from '../js/shared.js'
$(document).ready(function(){
    $('#idSendMsg011').click((e)=>{
        e.preventDefault();
        let formData = new FormData()
        formData.append('name', $('#con_firstName').val())
        formData.append('surname', $('#con_lastName').val())
        formData.append('email', $('#con_email').val())
        formData.append('phone', $('#con_phone').val())
        formData.append('message', $('#con_message').val())

        $.ajax({
            method:'POST',
            url:'/send-message/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:(res)=>{
                swalAlert('success', 'Envoyé', 'Message envoyé avec succès')
                $('#contact_form').trigger("reset");
                removeError($('#con_firstNameError'), $('#con_firstName'))
                removeError($('#con_lastNameError'), $('#con_lastName'))
                removeError($('#con_emailError'), $('#con_email'))
                removeError($('#con_phoneError'), $('#con_phone'))
                removeError($('#con_messageError'), $('#con_message'))

            },
            error:(err)=>{
                let tabErrors = err.responseJSON
                setError('name', tabErrors, $('#con_firstNameError'), $('#con_firstName'))
                setError('surname', tabErrors, $('#con_lastNameError'), $('#con_lastName'))
                setError('email', tabErrors, $('#con_emailError'), $('#con_email'))
                setError('phone', tabErrors, $('#con_phoneError'), $('#con_phone'))
                setError('message', tabErrors, $('#con_messageError'), $('#con_message'))
            }
        })
    })
})