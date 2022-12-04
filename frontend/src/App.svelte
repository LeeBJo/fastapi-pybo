<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"   //게시글 상세보기
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from './components/Navigation.svelte';
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import QuestionModify from "./routes/QuestionModify.svelte"
  import AnswerModify from "./routes/AnswerModify.svelte"

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
    // '/manager' : 매니저 홈
    // '/manager/user-list' : 매니저 페이지 유저 리스트
    // '/manager/user-detail/:username' : 매니저 유저 정보
    // '/manager/user-create' : 관리자 회원 생성
    // '/manager/user-modify' : 관리자 회원 수정
    // '/manager/health-info-list' : 매니저 페이지 건강 정보 리스트
    // '/manager/health-info-detail/:health_info_id' : 매니저 상세 건강 정보
    // '/manager/health-info-create' : 관리자 건강 정보 생성

  }
</script>

<Navigation/>
<Router {routes}/>

