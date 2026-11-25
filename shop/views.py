from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Brand, Frame, Customer, Order, Review

def home(request):
    reviews = (Review.objects.filter(approved=True)
               .select_related('order__customer__user', 'order__frame')[:6])
    return render(request, 'shop/index.html',
                  {'brands': Brand.objects.all(), 'reviews': reviews})

def all_frames(request):
    frames = Frame.objects.select_related('brand')
    return render(request, 'shop/frames.html',
                  {'frames': frames, 'brands': Brand.objects.all(), 'title': 'All frames'})

def brand_frames(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    return render(request, 'shop/frames.html',
                  {'frames': brand.frames.all(), 'brands': Brand.objects.all(), 'title': brand.name})

def frame_detail(request, frame_id):
    frame = get_object_or_404(Frame, id=frame_id)
    return render(request, 'shop/frame_detail.html', {'frame': frame})

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        user = User.objects.create_user(
            username=d['phone'], password=d['password'], first_name=d['name'])
        Customer.objects.create(
            user=user, phone=d['phone'], age=d['age'],
            gender=d['gender'], consent=d['consent'])
        login(request, user)
        return redirect('home')
    return render(request, 'shop/register.html', {'form': form})

@login_required
def order_frame(request, frame_id):
    frame = get_object_or_404(Frame, id=frame_id, in_stock=True)
    customer = getattr(request.user, 'customer', None)
    if customer is None:
        return redirect('register')
    error = ''
    if request.method == 'POST':
        shop = request.POST.get('shop')
        if shop in dict(Order.SHOPS):
            Order.objects.create(
                customer=customer, frame=frame, price=frame.price,
                shop=shop, note=request.POST.get('note', '')[:200])
            return redirect('my_orders')
        error = 'Please choose a shop for pickup.'
    return render(request, 'shop/order_frame.html',
        {'frame': frame, 'shops': Order.SHOPS, 'error': error,
         'advance': frame.price / 2})


@login_required
def my_orders(request):
    customer = getattr(request.user, 'customer', None)
    orders = customer.orders.select_related('frame__brand') if customer else []
    return render(request, 'shop/my_orders.html', {'orders': orders})

@login_required
def write_review(request, order_id):
    order = get_object_or_404(Order, id=order_id,
                              customer__user=request.user, status='PU')
    if hasattr(order, 'review'):
        return redirect('my_orders')
    error = ''
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 0))
        except ValueError:
            rating = 0
        feedback = request.POST.get('feedback', '').strip()[:400]
        if 1 <= rating <= 5 and feedback:
            Review.objects.create(order=order, rating=rating,feedback=feedback, approved=True)
            return redirect('my_orders')
        error = 'Please choose a rating and write a short review.'
    return render(request, 'shop/review_form.html', {'order': order, 'error': error})

@staff_member_required
def dashboard(request):
    active = Order.objects.exclude(status='CN')

    monthly = (active.annotate(m=TruncMonth('created'))
               .values('m').annotate(n=Count('id')).order_by('m'))
    brands = (active.values('frame__brand__name')
              .annotate(n=Count('id')).order_by('-n')[:5])
    frames = (active.values('frame__name')
              .annotate(n=Count('id')).order_by('-n')[:5])
    status = Order.objects.values('status').annotate(n=Count('id'))
    labels = dict(Order.STATUS)

    charts = {
        'months': [x['m'].strftime('%b %Y') for x in monthly],
        'month_counts': [x['n'] for x in monthly],
        'brands': [x['frame__brand__name'] for x in brands],
        'brand_counts': [x['n'] for x in brands],
        'frames': [x['frame__name'] for x in frames],
        'frame_counts': [x['n'] for x in frames],
        'status': [labels[x['status']] for x in status],
        'status_counts': [x['n'] for x in status],
    }
    revenue = Order.objects.filter(status='PU').aggregate(s=Sum('price'))['s'] or 0
    stats = {
        'orders': Order.objects.count(),
        'picked_up': Order.objects.filter(status='PU').count(),
        'revenue': revenue,
        'customers': Customer.objects.count(),
        'repeat': Customer.objects.annotate(n=Count('orders')).filter(n__gt=1).count(),
        'rating': Review.objects.aggregate(a=Avg('rating'))['a'],
    }
    return render(request, 'shop/dashboard.html', {'stats': stats, 'charts': charts})