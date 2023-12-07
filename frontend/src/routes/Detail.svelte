<script>
    import fastapi from "../lib/api"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    export let params = {}
    $: if ($username) {
        console.log("Logged in user:", $username);
    } else {
        console.log("No logged in user");
    }
    let post_id = params.post_id

    let post = {content: ''}
    let content = ""
    function get_post() {
        fastapi("get", "/api/post/detail/" + post_id, {}, (json) => {
            post = json
            console.log("=====post====", post)
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

    function delete_post(_post_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/post/delete/" + _post_id
            let params = {
                post_id: _post_id
            }
            console.log("=delete_post params:===", params)
            fastapi('delete', url, {}, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function vote_post(_post_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/post/vote"
            let params = {
                post_id: _post_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_post()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }


</script>

<div class="container my-3">
    <!-- 글 -->
    <h2 class="border-bottom py-2">{post.title}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text"> {@html marked.parse(post.content)}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">작성자 : { post ? post.username : ""}</div>
                <div>작성 시간 : {post.created_time}</div>
                <div>수정 시간 : {post.updated_time}</div>
                <div>조회수 : {post.view_count}</div>
                <div>추천수 : {post.help_count}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click="{vote_post(post.post_id)}"> 
                    추천
                </button>
                {#if $username === post.username}
                <a use:link href="/post-modify/{post.post_id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                on:click={() => delete_post(post.post_id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>


</div>

