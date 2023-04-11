import {setError, swalLikeToast, swalAlert, toastAlert} from '../js/shared.js'
$(document).ready(()=>{
    
    if(user==='AnonymousUser'){
        $('#submitOrder').click((e)=>{
            e.preventDefault()
            let formData = new FormData();
            formData.append('name', $("#idName").val())
            formData.append('surname', $("#idSurname").val())
            formData.append('email', $("#idEmail").val())
            formData.append('phone', $("#idPhone").val())
            formData.append('country', $("#idCountry").val())
            formData.append('city', $("#idCity").val())
            formData.append('address', $("#idAddresse").val())
            formData.append('exactAddress', $("#idExactAddr").val())
            formData.append('methodPayment', $('#inputPayment:checked').val())
            $.ajax({
                method:'POST',
                url:'/confirm-order/',
                processData:false,
                contentType: false,
                headers:{'X-CSRFToken':csrftoken},
                data:formData,
                success:(res)=>{
                    let id = res['id']
                    window.location.href = '/close-order/'+id+'/'
                },
                error:(err)=>{
                    let tabErrors = err.responseJSON
                    setError('phone', tabErrors, $('#idPhoneError'), $('#idPhone'))
                    setError('country', tabErrors, $('#idCountryError'), $('#idCountry'))
                    setError('city', tabErrors, $('#idCityError'), $('#idCity'))
                    setError('address', tabErrors, $('#idAddressError'), $('#idAddresse'))
                    setError('email', tabErrors, $('#idEmailError'), $('#idEmail'))
                    setError('payment', tabErrors, $('#idPaymentError'), $('#idPaymentError'))
                }
            })
        })
    }
    else{

        $('#submitNewAddr').click((e)=>{
            e.preventDefault()
            let formData = new FormData();
            formData.append('name', $("#idName").val())
            formData.append('surname', $("#idSurname").val())
            formData.append('phone', $("#idPhone").val())
            formData.append('country', $("#idCountry").val())
            formData.append('city', $("#idCity").val())
            formData.append('address', $("#idAddresse").val())
            formData.append('exactAddress', $("#idExactAddr").val())
            formData.append('idSelectDefault', $('#idSelectDefault').prop('checked'))
            // console.log("the checked value is", $('#idSelectDefault').prop('checked'))
            $.ajax({
                method:'POST',
                url:'/register-address/',
                processData:false,
                contentType: false,
                headers:{'X-CSRFToken':csrftoken},
                data:formData,
                success:(res)=>{
                    window.location.reload();
                    toastAlert('success', 'Adresse ajoutée avec succès')
                },
                error:(err=>{
                    let tabErrors = err.responseJSON
                    setError('phone', tabErrors, $('#idPhoneError'), $('#idPhone'))
                    setError('country', tabErrors, $('#idCountryError'), $('#idCountry'))
                    setError('city', tabErrors, $('#idCityError'), $('#idCity'))
                    setError('address', tabErrors, $('#idAddressError'), $('#idAddresse'))
                })
            })
        })
        


        $("#submitOrder").click((e)=>{
            e.preventDefault()
            let formData = new FormData();
            formData.append('idAddress', $('#idAddress:checked').val())
            formData.append('idOrder', $('#idOrder').val())
            formData.append('methodPayment', $('#inputPayment:checked').val())
            $.ajax({
                method:'POST',
                url:'/confirm-order/',
                processData:false,
                contentType: false,
                headers:{'X-CSRFToken':csrftoken},
                data:formData,
                success:(res)=>{
                    window.location.href = '/close-order/'+$('#idOrder').val()+'/'
                },
                error:(err)=>{
                    let erro = err.responseJSON
                    if (erro['address'])
                        swalAlert('error', 'Ooopss...', erro['address'])
                    else
                        swalAlert('error', 'Ooopss...', erro['payment'])

                }
            })
        })
    }

    // *********************************** to apply coupon on the command ***********************************
    $('#applyCoupon').click((e)=>{
        e.preventDefault();
        let formData = new FormData();
        formData.append('valCoupon', $('#coupon_code').val())
        formData.append('idOrder', $('#idForOrder').val())
        $.ajax({
            method:'POST',
            url:'/apply-discount/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:function(res){
                if(res){
                    $('#idTotalReduction').html(`<span>${res['reduction']} Fcfa</span>`)
                    $('#idBiTotal').html(`<strong><span>${res['newBigTotal']} Fcfa</span></strong>`)
                    toastAlert('success', 'Coupon validé')
                }
            },
            error:(err)=>{
                let erro = JSON.parse(err.responseText)
                $("#validationServer03Feedback").html(erro['valueCoupon'])
            }
        })
    })

    $('#editProfile').click((e)=>{
        e.preventDefault();
        let formData = new FormData();
        formData.append('name', $('#nameProfile').val());
        formData.append('surname', $('#surnameProfile').val());
        formData.append('email', $('#emailProfile').val());
        formData.append('oldPass', $('#oldPassProfile').val());
        formData.append('password1', $('#password1Prodile').val());
        formData.append('password2', $('#confirmPassProfile').val());
        $.ajax({
            method:'POST',
            url:'/edit-profile/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:function(res){
                if (res ==='nothing') {
                }
                else{
                    swalLikeToast('success', 'Information modifiée avec succès')
                    window.location.reload()
                }
            },
            error:(err)=>{
                console.log(err)
                let tabErrors = err.responseJSON
                setError('name', tabErrors, $('#nameProfileError'), $('#nameProfile'))
                setError('surname', tabErrors, $('#surnameProfileError'), $('#surnameProfile'))
                setError('email', tabErrors, $('#emailProfileError'), $('#emailProfile'))
                setError('oldPassword', tabErrors, $('#oldPassProfileError'), $('#oldPassProfile'))
                setError('password1', tabErrors, $('#password1ProdileError'), $('#password1Prodile'))
                setError('password2', tabErrors, $('#confirmPassProfileError'), $('#confirmPassProfile'))
            }
        })
    })
})