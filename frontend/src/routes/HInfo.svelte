<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, keyword, is_login } from "../lib/store"      // page대신 건강정보 페이지

    let HInfo_list = []
    let size = 10               //페이지당 표시 갯수
    let total = 0
    let kw = ''         //검색어
    //토탈 건강정보 페이지로
    $: total_page = Math.ceil(total/size)   //변수앞에 $: 기호를 붙이면 해당 변수는 반응형 변수가 된다.
                                            //total 변수의 값이 API 호출로 인해 그 값이 변하면 total_page 변수의 값도 실시간으로 재계산된다

    function get_question_list() {  //get_user_list
        let params = {
            page: $page,            //건강정보 페이지
            size: size,
            keyword: $keyword,
        }
        fastapi('get', '/api/question/list', params, (json) => {        //HInfolist로
            question_list = json.question_list
            total = json.total
            kw = $keyword
        })
    }
        // Hinfo page로
    $:$page, $keyword, get_question_list()      //$page 또는 $keyword의 값이 변경되면 자동으로 get_question_list() 함수가 실행
</script>
<!--질문 목록 데이터가 "question_list"라는 이름으로 전달-->


<div class="container my-3">
    <div class="row my-3">
        <!-- 정보 추가로 -->
        <div class="col-6">
            <a use:link href="/question-create"     
                class="btn btn-primary {$is_login ? '' : 'disabled'}">정보추가</a>
        </div>
        <!-- 정보 검색 -->
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{kw}">  <!-- 구현시 정보 키워드, 정보 페이지-->
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
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
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        <!-- 건강정보 리스트 -->
        {#each question_list as question, i}
        <tr class="text-center">
            <td>{total - ($page * size) - i}</td>
            <td class="text-start">
                <!-- 건강정보 조회                          정보 제목 -->
                <a use:link href="/detail/{question.id}">{question.subject}</a>
            </td>
            <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>  <!-- 한국 날짜 형식 -->
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5} 
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->
</div>