<script>
    import fastapi from "../lib/api"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'

    export let params = {}

    let post_id = params.post_id
    let content = ""
    let post = {content: '', answers: []}


    function get_post() {
        fastapi("get", "/api/post/detail/" + post_id, {}, (json) => {
            post = json
            console.log(json)
        })
    }

    function get_reply() {
        fastapi("get", "/api/post/detail/" + reply_id, {}, (json) => {
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

    function delete_reply(_reply_id,) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/reply/delete/" + _reply_id
            let params = {
                reply_id: _reply_id
            }
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

    function vote_reply(_reply_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/reply/vote"
            let params = {
                reply_id: _reply_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_reply()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function add_reply_view_count(_post_id){
        let url = "/api/reply/view"
        let params = {
                post_id: _post_id
            }
        fastapi('post', url, params)
            .then(() => {           
            console.log("조회수 증가 성공!");
            })
            .catch(error => {
            console.error("조회수 증가 실패:", error);
            });
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
    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{post.answers.length}개의 답변이 있습니다.</h5>
    {#each post.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    <div>작성자 : {answer.username}</div>
                    <div>작성 시간 : {answer.created_time}</div>
                    <div>수정 시간 : {answer.updated_time}</div>
                    <div>조회수 : {answer.view_count}</div>
                    <div>추천수 : {answer.help_count}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click="{vote_reply(answer.reply_id)}"> 
                    추천
                </button>
                {#if $username === answer.username}
                <a use:link href="/reply-modify/{answer.reply_id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                on:click={() => delete_reply(answer.reply_id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>
    {/each}
    <!-- 답변 등록 -->
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} class="form-control" />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary" on:click="{post_reply}" />
    </form>

    


</div>

