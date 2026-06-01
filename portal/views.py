from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

from .models import User, Application, Review
from .forms import RegisterForm, ApplicationForm, ReviewForm


class RegisterView(View):
    def get(self, request):
        return render(request, 'portal/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'portal/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'portal/login.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином не найден')
            return render(request, 'portal/login.html')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.username == 'Admin26':
                return redirect('admin_panel')
            return redirect('dashboard')

        messages.error(request, 'Неверный пароль')
        return render(request, 'portal/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.username == 'Admin26':
            return redirect('admin_panel')
        applications = Application.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        return render(request, 'portal/dashboard.html', {
            'applications': applications,
            'reviews': reviews,
        })


class CreateApplicationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'portal/create_application.html', {'form': ApplicationForm()})

    def post(self, request):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, 'Заявка отправлена на рассмотрение')
            return redirect('dashboard')
        return render(request, 'portal/create_application.html', {'form': form})


class CreateReviewView(LoginRequiredMixin, View):
    def post(self, request, app_id):
        app = get_object_or_404(Application, id=app_id, user=request.user)
        if app.status != 'Обучение завершено' or hasattr(app, 'review'):
            messages.error(request, 'Отзыв можно оставить только после завершения обучения')
            return redirect('dashboard')
        Review.objects.create(
            user=request.user,
            application=app,
            text=request.POST.get('text', ''),
        )
        messages.success(request, 'Спасибо за отзыв!')
        return redirect('dashboard')


class AdminPanelView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.username != 'Admin26':
            messages.error(request, 'Доступ запрещен')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        applications = Application.objects.all().select_related('user')

        status_filter = request.GET.get('status')
        search = request.GET.get('search')
        sort = request.GET.get('sort', 'date')

        if status_filter and status_filter != 'all':
            applications = applications.filter(status=status_filter)
        if search:
            applications = applications.filter(user__username__icontains=search)

        if sort == 'date_asc':
            applications = applications.order_by('created_at')
        elif sort == 'course':
            applications = applications.order_by('course')
        elif sort == 'status':
            applications = applications.order_by('status')
        elif sort == 'user':
            applications = applications.order_by('user__username')
        else:
            applications = applications.order_by('-created_at')

        paginator = Paginator(applications, 5)
        page = request.GET.get('page', 1)
        applications_page = paginator.get_page(page)

        return render(request, 'portal/admin_panel.html', {
            'applications': applications_page,
            'status_choices': Application.STATUS,
            'status_filter': status_filter,
            'search': search,
            'sort': sort,
        })

    def post(self, request, app_id):
        app = get_object_or_404(Application, id=app_id)
        app.status = request.POST.get('status')
        app.save()
        messages.success(request, f'Статус заявки №{app_id} изменен')
        return redirect('admin_panel')
