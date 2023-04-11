import {setError, removeError, swalLikeToast} from '../js/shared.js'

$(document).ready(()=>{
    $('#commentBlogButton').click((e)=>{
        e.preventDefault();
        let formData = new FormData();
        formData.append('subject', $('#blogSubject').val())
        formData.append('message', $('#blogComment').val())
        formData.append('idBlog', $('#idForBlog').val())
        $.ajax({
            method:'POST',
            url:'/comment-blog/',
            processData:false,
            contentType: false,
            headers:{'X-CSRFToken':csrftoken},
            data:formData,
            success:(res)=>{
                swalLikeToast('success', 'Commentaire enregistré avec succès')
                window.location.reload()
            },
            error:(err)=>{
                let tabErrors = err.responseJSON
                setError('subject', tabErrors, $('#blogSubjectError'), $('#blogSubject'))
                setError('message', tabErrors, $('#blogCommentError'), $('#blogComment'))

            }
        })
    })
})