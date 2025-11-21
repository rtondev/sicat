export const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/fichas',
    name: 'Fichas',
    component: () => import('../views/Fichas.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/fichas/nova',
    name: 'NovaFicha',
    component: () => import('../views/NovaFicha.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: () => import('../views/Perfil.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/usuarios',
    name: 'AdminUsuarios',
    component: () => import('../views/AdminUsuarios.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/fichas',
    name: 'AdminFichas',
    component: () => import('../views/AdminFichas.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/bibliotecas',
    name: 'AdminBibliotecas',
    component: () => import('../views/AdminBibliotecas.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/bibliotecario',
    name: 'Bibliotecario',
    component: () => import('../views/Bibliotecario.vue'),
    meta: { requiresAuth: true, requiresBibliotecario: true }
  },
  {
    path: '/bibliotecario/solicitacao/:id',
    name: 'VerSolicitacao',
    component: () => import('../views/VerSolicitacao.vue'),
    meta: { requiresAuth: true, requiresBibliotecario: true }
  }
]

