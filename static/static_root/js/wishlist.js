import { swalLikeToast } from '../js/shared.js'


$(document).ready(()=>{
    $('.addWishList').click((e)=>{
        e.preventDefault();
        addWishlist(e.target.id)
        
    })

    $('.addWishListShop').click((e)=>{
        e.preventDefault();
        addWishlist(e.target.id)
    })

    $('.addWishListNew').click((e)=>{
        e.preventDefault();
        addWishlist(e.target.id)
    })

    $('.addWhislistBrand').click((e)=>{
        e.preventDefault();
        addWishlist(e.target.id)
    })

    $('.addWhislistBrandMain').click((e)=>{
        e.preventDefault();
        addWishlist(e.target.id)
    })

    $('.addWhislistBrandSecond').click((e)=>{
        e.preventDefault();
        addWishlist(e.target.id)
    })

    function addWishlist(idProd){
        let formData = new FormData()
        formData.append('idProd', idProd)
        $.ajax({
            method:'POST',
            url: '/add-wishlist/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:function(res){
                swalLikeToast('success', 'Article  ajouté dans la wishlist')
            },
            error:function(err){
                let erro = err.responseJSON
                swalLikeToast('error', erro['wish'])
            }
        })
    }

$('.removeWishlist').click((e)=>{
    e.preventDefault();
    let formData = new FormData();
    let id_product = e.target.id
    var index = parseInt($('table tr').index('tr')) + 1;
    formData.append('idProd', id_product);
   
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                method:'POST',
                url:'/delete-item-wishlist/',
                processData:false,
                contentType: false,
                headers:{'X-CSRFToken':csrftoken},
                data:formData,
                success:function(res){
                    if (res[ 'success'] == 'delete') {
                        if (document.getElementById('idTableWishlist')) {
                            document.getElementById('idTableWishlist').deleteRow(index) //delete row from table view cart
                        }
                        swalLikeToast('success', 'Article retiré de la liste de souhait')
                    }
                    if (res['lenList'] ===0) {
                        $("#idWIshlist011").html(`
                        <h1 class='text-center'>Votre liste de souhait est vide</h1>
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