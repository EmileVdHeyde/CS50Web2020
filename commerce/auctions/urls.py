from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
   ,path( "listing/<int:listing_id>",views.listing,name='listing')
   ,path( "categories",views.categories,name='categories')
   ,path( "watchlist",views.watchlist,name='watchlist')
   ,path("addlisting",views.addlisting,name='addlisting')
   ,path("categoriesindex/<int:id>",views.categoriesindex,name='categoriesindex')
   ,path("bidhistory",views.bidtransaction,name='bidhistory')
   ,path("post_comment/<int:pk>",views.postcomment,name='post_comment')
   ,path("post_bid/<int:pk>",views.postbid,name='post_bid')
   ,path("add_watchlist/<int:pk>",views.addwatchlist,name='add_watchlist')
]
