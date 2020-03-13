import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/home/home'
import Course from '@/views/course/course'
import Work_manage from '@/views/workmange/work_manage'
import Approval_manage from '@/views/workmange/Approval_manage'
import Job_history from '@/views/workmange/Job_history'

Vue.use(Router);

let router = new Router({
    routes: [
        {
            path: '/',
            name: 'Work_manage',
            component: Work_manage,
            meta: {
                title: '首页',
            }
        },
        {
            path: '/Work_manage',
            name: 'Work_manage',
            component: Work_manage,
            meta: {
                title: '工单管理',
            }
        },
        {
            path: '/Approval_manage',
            name: 'Approval_manage',
            component: Approval_manage,
            meta: {
                title: '审批管理',
            }
        },
        {
            path: '/Job_history',
            name: 'Job_history',
            component: Job_history,
            meta: {
                title: '工单历史',
            }
        },
        {
            path: '/home',
            name: 'home',
            component: Home,
            meta: {
                title: '首页',
            }
        },
        {
            path: '/course',
            name: 'course',
            component: Course,
            meta: {
                title: 'Course',
            }
        }
    ]
});

router.beforeEach((to, from, next) => {
    if (to.matched.length === 0) {
        from.path ? next({path: from.path}) : next('/');
    } else {
        next();
    }
});
export default router
