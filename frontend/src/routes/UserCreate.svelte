<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"

    let username = ''
    let password = ''
    let name = ''
    let birth = ''
    let sex = ''
    let address = ''
    let phone = ''

    function post_user(event) {
        event.preventDefault()
        let url = "/api/user/create"
        let params = {
            username: username,
            password: password,
            name : name,
            birth : birth,
            sex : sex,
            address : address,
            phone : phone
        }
        fastapi('post', url, params, 
            (json) => {
                push('/user-login')
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">회원 가입</h5>
    <form method="post">
        <div class="mb-3">
            <label for="username">아이디</label>
            <input type="text" class="form-control" id="username" bind:value="{username}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" id="password" bind:value="{password}">
        </div>
        <div class="mb-3">
            <label for="neme">이름</label>
            <input type="name" class="form-control" id="name" bind:value="{name}">
        </div>
        <div class="mb-3">
            <label for="birth">생년월일(YYMMDD)</label>
            <input type="birth" class="form-control" id="birth" bind:value="{birth}">
        </div>
        <div class="mb-3">
            <label for="sex">성별(male/female)</label>
            <input type="sex" class="form-control" id="sex" bind:value="{sex}">
        </div>
        <div class="mb-3">
            <label for="address">주소</label>
            <input type="address" class="form-control" id="address" bind:value="{address}">
        </div>
        <div class="mb-3">
            <label for="phone">전화번호(010-xxxx-xxxx)</label>
            <input type="phone" class="form-control" id="phone" bind:value="{phone}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{post_user}">생성하기</button>
    </form>
</div>
