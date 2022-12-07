<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    export let params = {}
    const username = params.username          // 유저 이름

    let error = {detail:[]}
    //유저의 속성들
    let _username = ''
    let email = ''
    let alarmAccepted = false

    //유저 디테일로 변경
    fastapi("get", "/api/user/detail/" + username, {}, (json) => {
        _username = json.username
        email = json.email
        alarmAccepted = alarmAccepted
    })

    //update_유저
    function update_user(event) {
        event.preventDefault()
        let url = "/api/user/update"            // fastapi update 추가
        let params = {
            username: username,
            email: email,
            alarmAccepted: alarmAccepted,
        }
        fastapi('put', url, params, 
            (json) => {
                push('/user-detail-mgr/'+username)       
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">정보 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <!-- 유저 정보 표시-->
        <div class="mb-3">
            <label for="subject">이름</label>           <!-- 유저이름 -->
            <input type="text" class="form-control" bind:value="{_username}">
        </div>
        <div class="mb-3">
            <label for="subject">email</label>           <!-- 이메일 -->
            <input type="text" class="form-control" bind:value="{email}">
        </div>
        <!-- 비밀번호 확인
        <div class="mb-3">
            <label for="subject">제목</label>           
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
         -->
        <!-- 새 비밀번호
        <div class="mb-3">
            <label for="subject">제목</label>            
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        -->
        <div class="mb-3">
            <label for="email">이메일 수신 동의 여부</label>        <!--이메일 수신 동의여부-->
            <input type="checkbox"  id="alarmAccepted" bind:checked="{alarmAccepted}">
        </div> 
        <button class="btn btn-primary" on:click="{update_user}">수정하기</button>
    </form>
</div>