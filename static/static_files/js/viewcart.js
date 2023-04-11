import { swalLikeToast} from '../js/shared.js'
$(document).ready(function(){
    let newVal = 1
     // ***************************************** UPDATED CART ********************************************
     $('.cart-plus-minus').append(
        '<div class="dec qtybutton"><i class="fa fa-minus"></i></div>\
        <div class="inc qtybutton"><i class="fa fa-plus"></i></div>'
    );
    $('.qtybutton').on('click', function (e) {
        let formData = new FormData()
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 1) {
                newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 1;
            }
        }
        $button.parent().find('input').val(newVal);
    });

    $('.updateCart').click(function(e){
        let formData = new FormData();
        let idProd = $(this).attr('id')
        let idOrder = document.getElementById("idForOrder").value
        
       if(user === 'AnonymousUser') {
           formData.append('idProd', idProd)
           formData.append('qte', newVal)
           $.ajax({
            method:'POST',
            url:'/update-quantity-item/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:function(res){
                if (res) {
                    // let total = res['bigTotal']
                    // $('#idForBigTotal').html(`
                    // <strong>${total} Fcfa</strong>
                    // `)
                    // $("td[id^=" + 'idSubTotal' + "]").html(`
                    // <strong>${total} Fcfa</strong>
                    // `)
                    // let result = JSON.parse(res['data'])
                    // for(let resul in result){
                    //     let subtotal = result[resul]['fields']['total']
                    // }
                    swalLikeToast('success', 'Quantité mise à jour avec succès')
                }
            }
        })
           
           
           
           
           
        }
        else{
            formData.append('idProd', idProd)
            formData.append('idOrder', idOrder)
            formData.append('qte', newVal)
            $.ajax({
                method:'POST',
                url:'/update-quantity-item/',
                processData:false,
                contentType: false,
                headers:{'X-CSRFToken':csrftoken},
                data:formData,
                success:function(res){
                    if (res) {
                        // let total = res['bigTotal']
                        // $('#idForBigTotal').html(`
                        // <strong>${total} Fcfa</strong>
                        // `)
                        // $("td[id^=" + 'idSubTotal' + "]").html(`
                        // <strong>${total} Fcfa</strong>
                        // `)
                        // let result = JSON.parse(res['data'])
                        // for(let resul in result){
                        //     let subtotal = result[resul]['fields']['total']
                        // }
                        swalLikeToast('success', 'Quantité mise à jour avec succès')
                    }
                }
            })
       }

    })
    
    // ****************************** update cart quatity ***********************************
    $('.updateBucket').click(()=>{
        window.location.reload()
    })

    // ****************************************** DELETE ITEM FOR CONNECTED **************************************
    $('.deleteId').click((e)=>{
        e.preventDefault();
        var index = parseInt($('table tr').index('tr')) + 1;
        var id_product = e.target.id;
        let formData = new FormData();
        let idOrder = document.getElementById('idForOrder').value
        formData.append('idOrder', idOrder);
        formData.append('idProd', id_product);
       
        var recountRows = function(){ //update index of table
            $('.indexCount').each(function(){
                $(this).html(index);
                index++
            })
        }
        Swal.fire({
            title: 'Êtes vous sûr de supprimer?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            cancelButtonText: 'Non!',
            confirmButtonText: 'Oui, supprimer!'
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'/delete-item-from-order/',
                    processData:false,
                    contentType: false,
                    headers:{'X-CSRFToken':csrftoken},
                    data:formData,
                    success:function(res){
                        if (res['success']==='delete') {
                            if (document.getElementById('idTableCart')) {
                                document.getElementById('idTableCart').deleteRow(index) //delete row from table view cart
                            }
                            $('#idViewCartItem').remove() //remove item from the icon cart at the top
                            recountRows() //to update the index
                            swalLikeToast('success', res['title'].toUpperCase() + ' supprimé(e) avec succès')
                            $('#idForBigTotal').html(`
                            <strong>${res['total']} Fcfa</strong>
                            `)
                            $('#idForBigTotals').html(`
                            <strong>${res['total']} Fcfa</strong>
                            `)
                            $('#idQteItem').html(`
                                <strong>${res['itemsCount']}</strong>
                            `)
                            $('#idQteItemm').html(`
                                <strong>${res['itemsCount']}</strong>
                            `)
                        }
                        if (res['total'] ===0) {
                            document.getElementById('showBox').style.display = 'none'
                            document.getElementById('showPayment').style.display = 'none'
                            $("#idCart01").html(`
                                <h1 class='text-center'>Votre panier est vide</h1>
                            `)
                            $('#idCartTemplate').html(`
                                <h1 class='text-center'>Votre panier est vide</h1>

                            `)
                        }
                    }
        
                })
                Swal.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
            }
          })
    })

    // ****************************************** DELETE ITEM FOR ANONYMOUS **************************************
    $('.deleteIdAnonymous').click((e)=>{
        e.preventDefault();
        var index = parseInt($('table tr').index('tr')) + 1;
        var id_product = e.target.id;
        let formData = new FormData();
        formData.append('idProd', id_product);
       
        var recountRows = function(){ //update index of table
            $('.indexCountAnonymous').each(function(){
                $(this).html(index);
                index++
            })
        }
        Swal.fire({
            title: 'Êtes vous sûr de supprimer?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonText: 'Non!',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Oui, supprimer!'
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'/delete-item-from-order/',
                    processData:false,
                    contentType: false,
                    headers:{'X-CSRFToken':csrftoken},
                    data:formData,
                    success:function(res){
                        if (res['success']==='delete') {
                            
                            if (document.getElementById('idTableCartAnonymous')) {
                                document.getElementById('idTableCartAnonymous').deleteRow(index) //delete row from table view cart
                            }
                            $('#idViewCartItemAnonymous').remove() //remove item from the icon cart at the top
                            recountRows() //to update the index
                            swalLikeToast('success', 'Article supprimé(e) avec succès')
                            // $('#idForBigTotal').html(`
                            // <strong>${res['total']} Fcfa</strong>
                            // `)
                            // change total in the header cart
                            $('#idForBigTotals').html(`
                            <strong>${res['total']} Fcfa</strong>
                            `)
                            //change total in the cart template
                            $('#idForBigtotalT').html(` 
                            <strong>${res['total']} Fcfa</strong>
                            `)
                            $('#idQteItemAnonym').html(`
                                <strong>${res['itemsCount']}</strong>
                            `)
                            $('#idQteItemAnonymm').html(`
                                <strong>${res['itemsCount']}</strong>
                            `)
                        }
                        if (res['total'] ===0) {
                            document.getElementById('showBox').style.display = 'none'
                            document.getElementById('showPayment').style.display = 'none'
                            $("#idCart001").html(`
                                <h1 class='text-center'>Votre panier est vide</h1>

                            `)
                            $('#idCartTemplateAnonymous').html(`
                                <h1 class='text-center'>Votre panier est vide</h1>

                            `)
                        }
                    }
                    
                })
                Swal.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
            }
          })
    })
})



