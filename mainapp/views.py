from functools import reduce
from itertools import chain

import datetime
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View

from .models import Category, Customer, CartProduct, Product, Banner, CommentModel
from .mixins import CartMixin
from .forms import OrderForm, LoginForm, RegistrationForm, ChangePasswordForm, CommentForm, SupportForm
from .utils import recalc_cart

from specs.models import ProductFeatures


class MyQ(Q):
    default = 'OR'


class AboutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'about.html', context)


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        banners = Banner.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'banners': banners,
            'cart': self.cart
        }
        return render(request, 'base.html', context)


# class AddCommentView(CartMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         categories = Category.objects.all()
#         form = CommentForm(request.POST or None)
#         context = {
#             'cart': self.cart,
#             'categories': categories,
#             'form': form
#         }
#         return render(request, 'addComment.html', context)
#
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         form = CommentForm(request.POST or None)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.name = form.cleaned_data['name']
#             new_comment.generalDescription = form.cleaned_data['generalDescription']
#             new_comment.comment = form.cleaned_data['comment']
#             new_comment.save()
#             messages.add_message(request, messages.INFO, "Коментар доданий")


class SupportView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = SupportForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'support.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = SupportForm(request.POST or None)
        if form.is_valid():
            new_supp = form.save(commit=False)
            new_supp.name = form.cleaned_data['name']
            new_supp.contact = form.cleaned_data['contact']
            new_supp.description = form.cleaned_data['description']
            new_supp.save()
            messages.add_message(request, messages.INFO, "Заявка буде оброблена найближчим часов, адміністратор з вами зв'яжиться.")
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/support/')


class ChangePasswordView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = ChangePasswordForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'newPas.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            new_pas = form.save(commit=False)
            new_pas.login = form.cleaned_data['login']
            new_pas.email = form.cleaned_data['email']
            new_pas.password = form.cleaned_data['newPassword']
            new_pas.save()
            messages.add_message(request, messages.INFO, "Заявка буде оброблена найближчим часов, менеджер з вами зв'яжиться.")
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/newPas/')


class ProductDetailView(CartMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_object().category.__class__.objects.all()
        context['cart'] = self.cart
        context['comments'] = CommentModel.objects.all()
        context['form'] = CommentForm
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        form = CommentForm(request.POST or None)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = Product.objects.get(slug=product_slug)
            new_comment.name = form.cleaned_data['name']
            new_comment.generalDescription = form.cleaned_data['generalDescription']
            new_comment.comment = form.cleaned_data['comment']
            new_comment.save()
            messages.add_message(request, messages.INFO, "Коментар доданий")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CategoryDetailView(CartMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        category = self.get_object()
        context['cart'] = self.cart
        context['categories'] = self.model.objects.all()
        if not query and not self.request.GET:
            context['category_products'] = category.product_set.all()
            return context
        if query:
            products = category.product_set.filter(Q(title__icontains=query))
            context['category_products'] = products
            return context
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        q_condition_queries = Q()
        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
            else:
                q_condition_queries.add(Q(**{'value': value}), Q.OR)
        pf = ProductFeatures.objects.filter(
            q_condition_queries
        ).prefetch_related('product', 'feature').values('product_id')
        products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
        context['category_products'] = products
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успішно доданий до кошику!")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успішно видалений кошику!")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кількість успішно змінена!")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            # new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO,
                                 "Замовлення успішно оформленно! Менерджер незабаром з вами зв'яжеться.")
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)


class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        context = {
            'customer': customer,
            'categories': categories,
            'cart': self.cart,
        }
        return render(request, 'profile.html', context)
