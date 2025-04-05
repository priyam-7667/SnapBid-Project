from django.urls import path
from .import views

urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("states",views.states,name="states"),
    path("delState",views.delState,name="delState"),
    path("updState",views.updState,name="updState"),
    path("citys",views.citys,name="citys"),
    path("delCity",views.delCity,name="delCity"),
    path("updCity",views.updCity,name="updCity"),
    path("categorys",views.categorys,name="categorys"),
    path("delCategory",views.delCategory,name="delCategory"),
    path("updCategory",views.updCategory,name="updCategory"),
]