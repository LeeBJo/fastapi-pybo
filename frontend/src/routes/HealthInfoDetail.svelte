<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')


    export let params = {}
    let health_info_id = params.health_info_id
    let health_info = {subject:'', content:'', link:''}
    let content = ""
    let error = {detail:[]}

    function get_health_info() {
        fastapi("get", "/api/health_info/detail/" + health_info_id, {}, (json) => {
            health_info = json
        })
    }

    get_health_info()

    //정보 삭제
    function delete_health_info(_health_info_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/health_info/delete"
            let params = {
                health_info_id: _health_info_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/health-info-list')          
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<div class="container my-3">
    <!-- 건강정보 -->
    <h2 class="border-bottom py-2">{health_info.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">
                {@html marked.parse(health_info.content)}
            </div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2 text-start">
                    <div>{moment(health_info.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_health_info(health_info_id)}>삭제</button>
            </div>
        </div>
    </div>

    <!--링크 수정필요****** '/manager' : 매니저 홈 -->
    <button class="btn btn-secondary" on:click="{() => {
        push('/')              
    }}">목록으로</button>

</div>