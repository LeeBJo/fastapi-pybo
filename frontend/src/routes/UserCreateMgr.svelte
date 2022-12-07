<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    //입력 항목
    let error = {detail:[]} 
    let username = ''               
    let password1 = ''
    let password2 = ''
    let email = ''
    let alarmAccepted = false
    let authority = false

    function post_user_mgr(event) {
        event.preventDefault()
        let url = "/api/user/create"
        let params = {
            username: username,
            password1: password1,
            password2: password2,
            email: email,
            alarmAccepted: alarmAccepted,
            authority: authority
        }
        fastapi('post', url, params, 
            (json) => {
                push('/user-list')     //'/manager/user-list' : 매니저 페이지 유저 리스트
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">회원 가입</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" id="username" bind:value="{username}">
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" class="form-control" id="password1" bind:value="{password1}">
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" class="form-control" id="password2" bind:value="{password2}">
        </div>
        <div class="mb-3">
            <label for="email">이메일</label>
            <input type="text" class="form-control" id="email" bind:value="{email}">
        </div>
        <div class="mb-3">
            <label for="email">이메일 수신 동의 여부</label>
            <input type="checkbox"  id="alarmAccepted" bind:checked="{alarmAccepted}">
        </div> 
        <div class="mb-3">
            <label for="email">관리자 권한 승인</label>
            <input type="checkbox"  id="alarmAccepted" bind:checked="{authority}">
        </div> 
        <button type="submit" class="btn btn-primary" on:click="{post_user_mgr}">생성하기</button>
    </form>
</div>