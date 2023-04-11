$(document).ready(function(){
    const searchInput = document.querySelector("#searchInput");
    const divNoApi = document.querySelector(".bigDivNoApi");
    const divApi = document.querySelector(".bigDivApi");
    const pagination = document.querySelector(".pagination-area");
    const bodyApi = document.querySelector(".bodyApi");
    const url = '/media/';

   if(searchInput){
       divApi.style.display = 'none';
        searchInput.addEventListener('keyup', (e)=>{
            const wordSearch = e.target.value;
            if(wordSearch.trim().length>0){
                pagination.style.display='none';
                bodyApi.innerHTML = '';
                fetch('/shop/', {
                    body: JSON.stringify({keySearch:wordSearch}),
                    method:'POST',
                })
                .then((res)=> res.json())
                .then((data)=>{
                    console.log("the data are", data)
                    divApi.style.display = 'block';
                    divNoApi.style.display = 'none';
                    if (data.length === 0) {
                        divApi.innerHTML='Aucun resultat'
                    }else{
                        data.forEach(item => {
                            bodyApi.innerHTML+=`
                            <div class="col-md-4 col-6">
                                <div class="product-item">
                                    <div class="product-img">
                                        <a href="{% url 'home:detailProd' product.id %}">
                                            <img width="270px" height="200px" class="primary-img" src="${url + item.mainImg}" alt="Product Images">
                                            <img width="270px" height="200px" class="secondary-img" src="${url + item.secondImg}" alt="Product Images">
                                        </a>
                                        <div class="product-add-action">
                                            <ul>
                                                
                                                <li>
                                                    <a id="${item.id}" href="cart.html" data-tippy="Ajouter au panier" class="addCartShop" data-tippy-inertia="true" data-tippy-animation="shift-away" data-tippy-delay="50" data-tippy-arrow="true" data-tippy-theme="sharpborder">
                                                        <i id="{{product.id}}" class="pe-7s-cart"></i>
                                                    </a>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                    <div class="product-content">
                                        <a class="product-name" href="{% url 'home:detailProd' product.id %}">${item.title}</a>
                                        <div class="price-box pb-1">
                                            <span class="new-price">${item.price} Fcfa</span>
                                        </div>
                                        <div class="rating-box">
                                            <ul>
                                                <li><i class="fa fa-star"></i></li>
                                                <li><i class="fa fa-star"></i></li>
                                                <li><i class="fa fa-star"></i></li>
                                                <li><i class="fa fa-star"></i></li>
                                                <li><i class="fa fa-star"></i></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            `
                        });
                    }
                })
                // divApi.innerHTML = '';
                // $.ajax({
                //     url:'/shop/',
                //     method:'POST',
                //     data:{keySearch:wordSearch},
                //     success:(res)=>{
                //         if(res.length===0){
                //             divNoApi.style.display = 'none';
                //             pagination.style.display = 'none';
                //             divApi.innerHTML = 'Aucun résultat pour votre recherche';
                //         }
                //         else{
                //             divNoApi.style.display = 'none';
                //             pagination.style.display = 'none';
                //             divApi.innerHTML = 'Yes result';
                //             // res.forEach(item => {
                //             //     divApi.innerHTML += `
                //             //     <div class="col-md-4 col-sm-6">
                //             //         <div class="product-item">
                //             //             <div class="product-img">
                //             //                 <a href="{% url 'home:detailProd' product.id %}">
                //             //                     <img width="270px" height="300px" class="primary-img" src="${url + item.mainImg}" alt="Product Images">
                //             //                     <img width="270px" height="300px" class="secondary-img" src="${url + item.secondImg}" alt="Product Images">
                //             //                 </a>
                //             //                 <div class="product-add-action">
                //             //                     <ul>
                //             //                         <li>
                //             //                             <a href="wishlist.html" data-tippy="Add to wishlist" data-tippy-inertia="true" data-tippy-animation="shift-away" data-tippy-delay="50" data-tippy-arrow="true" data-tippy-theme="sharpborder">
                //             //                                 <i class="pe-7s-like"></i>
                //             //                             </a>
                //             //                         </li>
                                                    
                //             //                         <li>
                //             //                             <a href="cart.html" data-tippy="Add to cart" data-tippy-inertia="true" data-tippy-animation="shift-away" data-tippy-delay="50" data-tippy-arrow="true" data-tippy-theme="sharpborder">
                //             //                                 <i class="pe-7s-cart"></i>
                //             //                             </a>
                //             //                         </li>
                //             //                     </ul>
                //             //                 </div>
                //             //             </div>
                //             //             <div class="product-content">
                //             //                 <a class="product-name" href="{% url 'home:detailProd' product.id %}">${item.title}</a>
                //             //                 <div class="price-box pb-1">
                //             //                     <span class="new-price">${item.price} Fcfa</span>
                //             //                 </div>
                //             //                 <div class="rating-box">
                //             //                     <ul>
                //             //                         <li><i class="fa fa-star"></i></li>
                //             //                         <li><i class="fa fa-star"></i></li>
                //             //                         <li><i class="fa fa-star"></i></li>
                //             //                         <li><i class="fa fa-star"></i></li>
                //             //                         <li><i class="fa fa-star"></i></li>
                //             //                     </ul>
                //             //                 </div>
                //             //             </div>
                //             //         </div>
                //             //     </div>`
                //             // });
                //         }
                //     }
                // })
            }
            else{
                divApi.style.display = 'none'
                divNoApi.style.display = 'block';
                pagination.style.display = 'block';
            }
        })
   }
})