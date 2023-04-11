import {spaceNumber, setError, swalLikeToast} from '../js/shared.js'
$(document).ready(()=>{
    let newVal = 1
    // **************************** add to cart ***************************************
    if (user === 'AnonymousUser') {
        $('.addCartId').click((e)=>{
            e.preventDefault();
            addToCartAnonymous($('#idForProduct').val(), $('#colorSelected').val(), $('#sizeSelected').val(), $('.addCartId'))
            
        })
        $('.addCartNewProd').click((e)=>{
            e.preventDefault();
            addToCartAnonymous(e.target.id, 'undefined', 'undefined', $('.addCartNewProd'));
        })
        $('.addCartNewProd').click((e)=>{
            e.preventDefault();
            addToCartAnonymous(e.target.id, 'undefined', 'undefined', $('.addCartNewProd'));
        })
        $('.addCartFeatured').click((e)=>{
            e.preventDefault();
            addToCartAnonymous(e.target.id, 'undefined', 'undefined', $('.addCartFeatured'));
        })
        $('.addCartShop').click((e)=>{
            e.preventDefault();
            addToCartAnonymous(e.target.id, 'undefined', 'undefined', $('.addCartShop'));
        })
    }
    else{
        $('.addCartId').click((e)=>{
            e.preventDefault();
            addToCart($('#idForProduct').val(), $('#colorSelected').val(), $('#sizeSelected').val(), $('.addCartId'));
        })

        $('.addCartFeatured').click((e)=>{
            e.preventDefault();
            addToCart(e.target.id, 'undefined', 'undefined', $('.addCartFeatured'));
        })

        $('.addCartIdNew').click((e)=>{
            e.preventDefault();
            addToCart(e.target.id, 'undefined', 'undefined', $('.addCartIdNew'));
        })

        $('.addCartNewProd').click((e)=>{
            e.preventDefault();
            addToCart(e.target.id, 'undefined', 'undefined', $('.addCartNewProd'));
        })

        $('.addCartShop').click((e)=>{
            e.preventDefault();
            addToCart(e.target.id, 'undefined', 'undefined', $('.addCartShop'));
        })

        $('.addCartMain').click((e)=>{
            e.preventDefault();
            addToCart(e.target.id, 'undefined', 'undefined', $('.addCartMain'))
        })

        $('.addCartSecond').click((e)=>{
            e.preventDefault();
            addToCart(e.target.id, 'undefined', 'undefined', $('.addCartSecond'))
        })
    }


    // *************************** ADD TO CART FOR CONNECTED USER **************************************
    // condfigurer le template uniquement au debut lorsquon rcoit lw resultat
    function addToCart(valueIdProd, valueIdColor, valueIdSize, btn){
        let formData = new FormData()
        formData.append('idProd', valueIdProd)
        formData.append('color', valueIdColor)
        formData.append('size', valueIdSize)
        formData.append('qte', newVal)
        let divAAddItems = document.querySelector('.cartAddItem')

        $.ajax({
            method:'POST',
            url: '/add-to-cart/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            beforeSend:function(){
                btn.prop('disabled', true); // disable button
            },
            success:function(res){
                btn.prop('disabled', false);
                let items = res['items'] ? JSON.parse(res['items']) : []
                //***************** */ hide button voir le panier and proccesder a l'achat *******************
                if (items){
                    document.getElementById('showBox').style.display = 'inline-block'
                    document.getElementById('showPayment').style.display = 'inline-block'
                }
                // ************************************* end *********************************
                if(res['message']==='updated'){
                    swalLikeToast('success', 'Quantité mise à jour avec succès')
                    divAAddItems.innerHTML = ''
                    $('#idForBigTotals').html(spaceNumber(res['bigTotal']) + ' Fcfa')
                    items.forEach(item => {
                        divAAddItems.innerHTML += `
                        <li class="minicart-product" id="idViewCartItem">
                        <a href="/product-detail/${item.fields.product}/" class="product-item_img">
                            <img width="50px", height="60px" src="${item.fields.pathImg}" alt="" srcset="">
                        </a>
                        <div class="product-item_content">
                            <a class="product-item_title" href="/product-detail/${item.fields.product}/">${item.fields.title}</a>
                            <span class="product-item_quantity">${item.fields.quantity} x ${spaceNumber(parseFloat(item.fields.price))} = ${spaceNumber(parseFloat(item.fields.total))} Fcfa</span>
                            ${item.fields.size ? '<strong>Taille </strong>' : ''}
                            ${item.fields.size ? item.fields.size : ''} <br>
                            ${item.fields.color ? '<strong>Couleur </strong>' : ''}
                            ${item.fields.color ? item.fields.color : ''} 
                        </div>
                    </li>
                        `
                    });
                }
                else{
                    $('#idQteItem').html(`
                        <strong>${res['nberItems']}</strong>
                    `)
                    //set item count for mobile responsive
                    $('#idQteItemm').html(` 
                        <strong>${res['nberItems']}</strong>
                    `)
                    divAAddItems.innerHTML = ''
                    $('#idForBigTotals').html(spaceNumber(res['bigTotal']) + ' Fcfa')
                    items.forEach(item => {
                        divAAddItems.innerHTML += `
                        <li class="minicart-product" id="idViewCartItem">
                        <a href="/product-detail/${item.fields.product}/" class="product-item_img">
                            <img width="50px", height="60px" src="${item.fields.pathImg}" alt="" srcset="">
                        </a>
                        <div class="product-item_content">
                            <a class="product-item_title" href="/product-detail/${item.fields.product}/">${item.fields.title}</a>
                            <span class="product-item_quantity">${item.fields.quantity} x ${spaceNumber(parseFloat(item.fields.price))} = ${spaceNumber(parseFloat(item.fields.total))} Fcfa</span>
                            ${item.fields.size ? '<strong>Taille </strong>' : ''}
                            ${item.fields.size ? item.fields.size : ''} <br>
                            ${item.fields.color ? '<strong>Couleur </strong>' : ''}
                            ${item.fields.color ? item.fields.color : ''} 
                        </div>
                    </li>
                        `
                    });
                    swalLikeToast('success', 'Produit ajouté avec succès')
                }
            },
            error:function(err){
                Swal.fire(
                    'The Internet?',
                    'That thing is still around?',
                    'question'
                  )
            }
        })

    }
    // ***************************** END ************************************************************
    
    // *********************************** ADD TO CART FOR ANONYMOUS USER ******************************
    function addToCartAnonymous(valueIdProd, valueIdColor, valueIdSize, btn){
        let divAAddItems = document.querySelector('.cartAddItems')
        let formData = new FormData()
            formData.append('idProd', valueIdProd)
            formData.append('color', valueIdColor)
            formData.append('size', valueIdSize)
            formData.append('qte', newVal)
            $.ajax({
                method:'POST',
                url: '/add-to-cart/',
                processData:false,
                contentType: false,
                headers:{'X-CSRFToken':csrftoken},
                data:formData,
                beforeSend:function(){
                    btn.prop('disabled', true); // disable button
                },
                success:(res)=>{
                    let data = Object.entries(res['data'])
    //***************** */ hide button voir le panier and proccesder a l'achat *******************
                    if (data){
                        document.getElementById('showBox').style.display = 'inline-block'
                        document.getElementById('showPayment').style.display = 'inline-block'
                    }
    // ***************************** END ************************************************************
                    $('#idForBigTotals').html(`${res['bigTotal']} Fcfa`)
                    $('#idQteItemAnonymm').html(`${res['count']}`)
                    $('#idQteItemAnonym').html(`${res['count']}`)
                    divAAddItems.innerHTML = ''
                    data.forEach(element => {
                        divAAddItems.innerHTML += `
                        <li class="minicart-product" id="idViewCartItem">
                        <a href="/product-detail/${element[0]}/" class="product-item_img">
                            <img width="50px", height="60px" src="${element[1]['path']}" alt="" srcset="">
                        </a>
                        <div class="product-item_content">
                            <a class="product-item_title" href="/product-detail/${element[0]}/">${element[1]['title']}</a>
                            <span class="product-item_quantity">${element[1]['qte']} x ${spaceNumber(parseFloat(element[1]['price']))} = ${spaceNumber(parseFloat(element[1]['subTotal']))} Fcfa</span>
                            ${element[1]['size'] ? '<strong>Taille </strong>' : ''}
                            ${element[1]['size'] ? element[1]['size'] : ''} <br>
                            ${element[1]['color'] ? '<strong>Couleur </strong>' : ''}
                            ${element[1]['color'] ? element[1]['color'] : ''} 
                        </div>
                        
                    </li>
                        `
                    });
                    
                    btn.prop('disabled', false); // disable button
                    if (res['message']==='updated') {
                        swalLikeToast('success', 'Quantité mise à jour avec succès')
                    }else{
                        swalLikeToast('success', 'Produit ajouté avec succès')
                    }
                }
            })

    }
    
    // ***************************** END ************************************************************

   

    // ********************************** retrieve quantity *********************************
    $('.cart-plus-minus').append(
        '<div class="dec qtybutton"><i class="fa fa-minus"></i></div><div class="inc qtybutton"><i class="fa fa-plus"></i></div>'
    );
    $('.qtybutton').on('click', function () {
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
    // *************************************** END ***************************************************

    $('#submitCommentProd').click((e)=>{
        e.preventDefault();
        let formData = new FormData()
        formData.append('idProd', $('#idForProduct').val())
        formData.append('comentProd', $('#commentProd').val())
        $.ajax({
            method:'POST',
            url: '/post-comment/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:function(res){
                swalLikeToast('success', 'Commentaire ajouté');
                window.location.reload();
            },
            error:(err)=>{
                let tabErrors = err.responseJSON
                setError('comment', tabErrors, $('#errorMsgProd'), $('#commentProd'))
            }
        })
        // console.log('clicked', $('#idForProduct').val())
    })
})


