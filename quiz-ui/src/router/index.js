import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuizPage from '../views/quiz/QuizPage.vue'
import QuestionManager from '../views/quiz/QuestionManager.vue'
import ScoreDisplay from '../views/quiz/ScoreDisplay.vue'
import AdminLogin from '../views/admin/AdminLogin.vue'
import AdminPanel from '../views/admin/AdminPanel.vue'
import AdminDetailQuestion from '../views/admin/AdminDetailQuestion.vue'
import AdminEditQuestion from '../views/admin/AdminEditQuestion.vue'
import AdminAddQuestion from '../views/admin/AdminAddQuestion.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: QuizPage
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionManager
    },
    {
      path: '/scoreboard',
      name: 'scoreboard',
      component: ScoreDisplay
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminLogin
    },
    {
      path: '/admin-panel',
      name: 'adminPanel',
      component: AdminPanel
    },
    {
      path: '/detail-question',
      name: 'detailQuestion',
      component: AdminDetailQuestion
    },
    {
      path: '/edit-question',
      name: 'editQuestion',
      component: AdminEditQuestion
    },
    {
      path: '/new-question',
      name: 'addQuestion',
      component: AdminAddQuestion
    }
  ]
})

export default router
