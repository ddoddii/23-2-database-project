<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import QuestionModify from "./routes/QuestionModify.svelte"


  const routes = {
    '/': Home,
    '/detail/:post_id': Detail,
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/post-modify/:post_id': QuestionModify,
  }
</script>
<Navigation />
<Router {routes}/>
