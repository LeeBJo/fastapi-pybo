<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"   //게시글 상세보기
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from './components/Navigation.svelte'
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import QuestionModify from "./routes/QuestionModify.svelte"
  import AnswerModify from "./routes/AnswerModify.svelte"
  import HealthInfoList from './routes/HealthInfoList.svelte'
  import HealthInfoCreate from './routes/HealthInfoCreate.svelte'
  import HealthInfoDetail from './routes/HealthInfoDetail.svelte'
  import UserlistMgr from './routes/UserlistMgr.svelte'
  import UserCreateMgr from './routes/UserCreateMgr.svelte'
  import UserDetailMgr from './routes/UserDetailMgr.svelte'
  import UserModifyMgr from './routes/UserModifyMgr.svelte'     //수정필요
  import RecommendHome from "./routes/RecommendHome.svelte";
  //import RecommendDetail from "./routes/RecommendDetail.svelte";
  //import RecommendQuestionCreate from "./routes/RecommendQuestionCreate.svelte";
  //----------------------------------import UserCreateMgr from './routes/UserCreateMgr.svelte';
  //----------------------------------import UserDetailMgr from './routes/UserDetailMgr.svelte';
  //----------------------------------import UserModifyMgr from './routes/UserModifyMgr.svelte';
  //----------------------------------import UserlistMgr from './routes/UserlistMgr.svelte';
  //----------------------------------import HealthInfoCreate from './routes/HealthInfoCreate.svelte';
  //----------------------------------import HealthInfoDetail from './routes/HealthInfoDetail.svelte';
  //----------------------------------import HealthInfoList from './routes/HealthInfoList.svelte';

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
    '/health-info-list' : HealthInfoList,
    '/health-info-create' : HealthInfoCreate,
    '/health-info-detail/:health_info_id' : HealthInfoDetail,
    '/user-list' : UserlistMgr,
    '/user-create-mgr' : UserCreateMgr,
    '/user-detail-mgr/:username' : UserDetailMgr,
    '/user-modify-mgr/:username' : UserModifyMgr,
    '/recommend-diet': RecommendHome
    //'/recommend-diet': RecommendHome,
    //'/recommend-diet-detail/:question_id': RecommendDetail,
    //'/recommend-diet-create': RecommendQuestionCreate
    // -----------------------------------------------------'/user-list' : 매니저 페이지 유저 리스트
    // -----------------------------------------------------'/user-detail/:username' : 매니저 유저 정보
    // -----------------------------------------------------'/user-create-mgr' : 관리자 회원 생성
    // ----------------------------'/user-modify-mgr' : 관리자 회원 수정
    // -----------------------------------------------------'/health-info-list' : 매니저 페이지 건강 정보 리스트
    // -----------------------------------------------------'/health-info-detail/:health_info_id' : 매니저 상세 건강 정보
    // -----------------------------------------------------'/health-info-create' : 관리자 건강 정보 생성

  }
</script>

<Navigation/>
<Router {routes}/>

