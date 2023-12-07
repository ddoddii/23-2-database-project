<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { is_login, keyword } from "../lib/store"
    let post_list = []
    let kw = ''
    function get_post_list() {
        let params = {
            keyword : kw
        }
        fastapi('get', '/api/post/list', params, (json) => {
            post_list = json
            console.log("post list", post_list)
        })
    }

</script>

<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/question-create" 
                class="btn btn-primary {$is_login ? '' : 'disabled'}">글 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{kw}">
                <button class="btn btn-outline-secondary" on:click={() => get_post_list(0)}>
                    찾기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>글쓴이</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each post_list as post, i}
        <tr class="text-center">
            <td>{i+1}</td>
            <td class="text-start">
                <a use:link href="/detail/{post.post_id}">{post.title}</a>
            </td>
            <td>{ post ? post.username : "" }</td>
            <td>{post.created_time}</td>
        </tr>
        {/each}
        </tbody>
    </table>
</div>
