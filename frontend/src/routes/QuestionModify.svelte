<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"

    export let params = {}
    const post_id = params.post_id

    let title = ''
    let content = ''

    fastapi("get", "/api/post/detail/" + post_id, {}, (json) => {
        title = json.title
        content = json.content
    })

    function update_post(event) {
        event.preventDefault()
        let url = "/api/post/update/" + post_id
        let params = {
            title: title,
            content: content,
        }
        let token = localStorage.getItem('access_token'); 

        // Set up headers for authentication
        let headers = {
            'Authorization': `Bearer ${token}`
        };
        
        fastapi('put', url, params, 
            (json) => {
                push('/detail/'+post_id)
            },
            (json_error) => {
                error = json_error
            },
            headers
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">글 수정</h5>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="title">제목</label>
            <input type="text" class="form-control" bind:value="{title}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_post}">수정하기</button>
    </form>
</div>
