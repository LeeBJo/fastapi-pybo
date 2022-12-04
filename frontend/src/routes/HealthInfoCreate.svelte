<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let link = ''

    function post_health_info(event) {
        event.preventDefault()
        let url = "/api/health_info/create"
        let params = {
            subject: subject,
            content: content,
            link: link
        }
        fastapi('post', url, params, 
            (json) => {
                push("/")               //링크수정필요*************** '/manager/health-info-list' : 매니저 페이지 건강 정보 리스트
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">건강 정보 등록</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <div class="mb-3">
            <label for="subject">원본링크</label>
            <input type="text" class="form-control" bind:value="{link}">
        </div>
        <button class="btn btn-primary" on:click="{post_health_info}">저장하기</button>
    </form>
</div>