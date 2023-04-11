import {setError, swalAlert, swalLikeToast} from '../js/shared.js'
$(document).ready(function(){
    $('#connectUserId').click((e)=>{
        e.preventDefault();
        let formData = new FormData();
        formData.append('email', $("#loginEmail").val())
        formData.append('password', $("#loginPassword").val())
        $.ajax({
            method:'POST',
            url: '/login-user/',
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            data:formData,
            headers:{'X-CSRFToken':csrftoken},
            success:function(res){
                if (res === '"success"') {
                    let previewPath = document.referrer
                    if(previewPath ===''){
                        window.location.href = '/'
                    }else{
                        window.location.href = document.referrer
                    }
                }
            },
            error:function(err){
                let error = JSON.parse(err.responseText)
                $('#loginEmail').addClass('is-invalid')
                $('#loginPassword').addClass('is-invalid')
                $('#textError').text(error['credential'])
            }
        })
    })

    // show the register form
    $('#registerUserId').click((e)=>{
        e.preventDefault();
        $('#containerRegister').css('display', 'inline')
        $('#containerLogin').css('display', 'none')
    })
    
    // show the login form
    $('#showConnectUser').click((e)=>{
        e.preventDefault();
        $('#containerRegister').css('display', 'none');
        $('#containerLogin').css('display', 'inline');
    })

    // create account
    $('#createAccount').click((e)=>{
        e.preventDefault();
        let approve = $('#dataConfidential').is(":checked");
        let formData = new FormData();
        formData.append('last_name', $("#clientName").val())
        formData.append('first_name', $("#clientSurname").val())
        formData.append('email', $("#clientEmail").val())
        formData.append('password', $("#clientPassword").val())
        formData.append('password_confirm', $("#clientConfirm").val())
        formData.append('type', 'Client')
        formData.append('type', 'Client')
        formData.append('approve', approve)
        $.ajax({
            method:'POST',
            url: '/api/register/',
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            data:formData,
            headers:{'X-CSRFToken':csrftoken},
            success : (res)=>{
                if (res) {
                    swalAlert('success', 'Compte créé', 'compte créé')
                }
            },
            error:(err)=>{
                let tabErrors = JSON.parse(err.responseText)
                setError('first_name', tabErrors, $('#clientSurnameError'), $('#clientSurname'))
                setError('last_name', tabErrors, $('#clientNameError'), $('#clientName'))
                setError('email', tabErrors, $('#clientEmailError'), $('#clientEmail'))
                setError('password', tabErrors, $('#clientPasswordError'), $('#clientPassword'))
                setError('password_confirm', tabErrors, $('#clientConfirmError'), $('#clientConfirm'))
                setError('approve', tabErrors, $('#clientApprovError'), $('#dataConfidential'))
            }
        })
    })

    // show space email for forget password
    $('#forgotPasswordId').click((e)=>{
        e.preventDefault();
        $('#containerLogin').css('display', 'none');
        $('#containerforgetPassword').css('display', 'inline');
    })

    // send email to reset password
    $('#resetPasswordId').click((e)=>{
        e.preventDefault()
        let formData = new FormData();
        formData.append('email', $('#emailResetPassword').val())
        formData.append('type', 'Client')
        $.ajax({
            method:'POST',
            url: '/api/forgot/',
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            data:formData,
            headers:{'X-CSRFToken':csrftoken},
            success: (res)=>{
                swalAlert('success', 'Réinitialiser mot de passe', 'Un email a été envoyé dans votre boite email pour réinitialiser votre mot de passe')
            },
            error: (err)=>{
                let tabErrors = JSON.parse(err.responseText)
                setError('email', tabErrors, $('#emailResetPasswordError'), $('#emailResetPassword'))
            }
        })
    })

    $('#resetPasswordId10').click((e)=>{
        e.preventDefault();
        let url = $(location). attr("href")
        let token = url.split('/reset/').pop().replace('/', '')
        let formData = new FormData();
        formData.append('password', $('#changePassword').val())
        formData.append('password_confirm', $('#changeConfirm').val())
        formData.append('token', token)
        $.ajax({
            method:'POST',
            url: '/api/reset/',
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            data:formData,
            headers:{'X-CSRFToken':csrftoken},
            success : (res)=>{
                if(res)
                Swal.fire('Mot de passe changé').then(()=>{
                    window.location.href = '/login/'
                })
            },
            error:(err)=>{
                let tabErrors = JSON.parse(err.responseText)
                if (tabErrors.hasOwnProperty('link')) {
                    swalLikeToast('error', 'Lien invalide')
                }
                else{
                    setError('password', tabErrors, $('#changePasswordError'), $('#changePassword'))
                    setError('password_confirm', tabErrors, $('#changeConfirmError'), $('#changeConfirm'))
                }
            }
        })
    })
})