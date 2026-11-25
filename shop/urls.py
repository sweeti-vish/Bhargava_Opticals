from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register('brands', api.BrandViewSet, basename='api-brand')
router.register('frames', api.FrameViewSet, basename='api-frame')
router.register('reviews', api.ReviewViewSet, basename='api-review')

urlpatterns = [
    path('', views.home, name='home'),
    path('frames/', views.all_frames, name='all_frames'),
    path('brand/<int:brand_id>/', views.brand_frames, name='brand_frames'),
    path('frame/<int:frame_id>/', views.frame_detail, name='frame_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('order/<int:frame_id>/', views.order_frame, name='order_frame'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('review/<int:order_id>/', views.write_review, name='write_review'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/dashboard/', api.dashboard_api, name='api_dashboard'),
    path('api/', include(router.urls)),
]