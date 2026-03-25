export const routerGuard = (to, from, next) => {
  const token = localStorage.getItem('access_token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  const requiresBibliotecario = to.matched.some(record => record.meta.requiresBibliotecario)
  const userRole = localStorage.getItem('user_role')

  if (requiresAuth && !token) {
    next('/login')
  } else if (requiresAdmin && userRole !== 'admin') {
    next('/dashboard')
  } else if (requiresBibliotecario && userRole !== 'bibliotecario') {
    next('/dashboard')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/dashboard')
  } else {
    next()
  }
}

