<script>
    import fastapi from "../lib/api"

    let users = []
    function get_users(){
        fastapi("get", "/users", {}, (json) => {
            users = json.users
            console.log(users)
        })
    }
    get_users()
</script>

<div>
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>ID</th>
            <th>사용자</th>
            <th>작성한 글 수</th>
            <th>작성한 답글 수</th>
        </tr>
        </thead>
        <tbody>
        {#each users as user (user.user_id)} <!-- Use user.user_id as the key for each iteration -->
        <tr class="text-center">
            <td>{user.user_id}</td>
            <td>{user.username}</td>
            <td>{user.post_count}</td>
            <td>{user.reply_count}</td>
        </tr>
        {/each}
        </tbody>
    </table>
</div>
