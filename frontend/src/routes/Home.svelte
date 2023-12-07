<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    let post_list = []

    function get_post_list() {
        fastapi('get', '/api/post/list', {}, (json) => {
            post_list = json
            console.log("post list", post_list)
        })
    }

    get_post_list()
</script>

<div class="container my-3">
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
    <a use:link href="/question-create" class="btn btn-primary">글 등록하기</a>
</div>
