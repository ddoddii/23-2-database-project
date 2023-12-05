<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'

    let post_list = []

    fastapi('get', '/api/post/list', {}, (json) => {
        post_list = json
    })
</script>

<ul>
    {#each post_list as post}
        <li><a use:link href="/detail/{post.id}">{post.subject}</a></li>
    {/each}
</ul>
