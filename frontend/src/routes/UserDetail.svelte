<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    //import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')


    export let params = {}
    let username = params.username
    let user = {username:'', email:'', authority:Boolean, alarmAccepted:Boolean}   //  유저가 넘기는 특성들로 수정
    let content = ""
    let error = {detail:[]}

    function get_user() {  
        fastapi("get", "/api/user/detail/" + username, {}, (json) => {   
            user = json
        })
    }

    get_user()
    

    //유저 삭제 도메인에 함수 추가
    function delete_user(_username) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/user/delete"                
            let params = {
                username: _username
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<div class="container my-3">
    <!-- 유저 정보 -->
    <h2 class="border-bottom py-2">{user.username}</h2>      <!-- 유저정보들로 수정-->
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">       <!--유저에서 넘기는 모든 정보를 표시-->
                {@html marked.parse(user.username)}        
                {@html marked.parse(user.email)}         
                {@html marked.parse(user.alarmAccepted)}          
                {@html marked.parse(user.authority)}       
            </div>
            <div class="my-3">  <!-- 수정, 삭제-->  <!--수정 페이지 필요******** -->
                <a use:link href="/user-modify/{user.username}"           
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_user(user.username)}>삭제</button>
            </div>
        </div>
    </div>

    
    <!--
    <button class="btn btn-secondary" on:click="{() => {
        push('/')
    }}">목록으로</button>
    -->

</div>