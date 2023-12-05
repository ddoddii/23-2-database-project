<script>
    import fastapi from "../lib/api"
    export let params = {}
    console.log("params",params)
    let post_id = params.post_id
    console.log("Received post_id:", post_id);

    let post = {}
    let content = ""
    console.log("Received post_id:", post_id);
    function get_post() {
        fastapi("get", "/api/post/detail/" + post_id, {}, (json) => {
            post = json
        })
    }

    get_post()

    function post_reply(event) {
        event.preventDefault()
        let url = "/api/reply/create/" + post_id
        let params = {
            content: content
        }
        fastapi('post', url, params, 
            (json) => {
                content = ''
                get_post()
            }
        )
    }
</script>

<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{post.title}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{post.content}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {post.created_date}
                </div>
            </div>
        </div>
    </div>

    
    <!-- 답변 등록 -->
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} class="form-control" />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary" on:click="{post_reply}" />
    </form>
</div>

