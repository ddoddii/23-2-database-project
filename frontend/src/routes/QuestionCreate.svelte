<script>
    import { push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import fastapi from "../lib/api"
    let title = ''
    let content = ''
    console.log("create user requset username: ", $username)
    function create_post(event) {
        event.preventDefault()
        let url = "/api/post/create"
        let params = {
            title: title,
            content: content,
        }
        
        fastapi('post', url, params, 
            (json) => {
                console.log("Post created by user ID:", json.user_id);
                push("/")
            },
            (json_error) => {
                error = json_error
            },
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">글 등록</h5>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="title">제목</label>
            <input type="text" class="form-control" bind:value="{title}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{create_post}">저장하기</button>
    </form>
</div>
