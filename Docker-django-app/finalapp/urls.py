from django.conf.urls import url 
from finalapp import views

urlpatterns = [ 
	url(r'^$', views.index, name='index'),
	url(r'^home/$',views.home,name='home'),
	url(r'^ask_images/$',views.ask_images,name='ask_images'),
	url(r'^search_images/$',views.search_images,name='search_images'),

	url(r'^ask_stop_container/$',views.ask_stop_container,name='ask_stop_container'),
	url(r'^stop_container/(?P<container_id>\S+)/$',views.stop_container,name='stop_container'),

	url(r'^deploy_war_app/(?P<ip_app>\S+)/$',views.deploy_war_app,name='deploy_war_app'),

	url(r'^ask_del_container/$',views.ask_del_container,name='ask_del_container'),
	url(r'^delete_container/(?P<container_id>\S+)/$',views.delete_container,name='delete_container'),

	url(r'^ask_start_container/$',views.ask_start_container,name='ask_start_container'),
	url(r'^start_container/(?P<container_id>\S+)/$',views.start_container,name='start_container'),

	url(r'^ask_restart_container/$',views.ask_restart_container,name='ask_restart_container'),
	url(r'^restart_container/(?P<container_id>\S+)/$',views.restart_container,name='restart_container'),

	url(r'^ask_search_images/$',views.ask_search_images,name='ask_search_images'),
	url(r'^search_images/(?P<search_name>\S+)/$',views.search_images,name='search_images'),

	url(r'^ask_del_commited_images/$',views.ask_del_commited_images,name='ask_del_commited_images'),
	url(r'^delete_commited_images/(?P<idd>\S+)/$',views.delete_commited_images,name='delete_commited_images'),

	url(r'^ask_del_images/$',views.ask_del_images,name='ask_del_images'),
	url(r'^delete_images/(?P<idd>\S+)/$',views.delete_images,name='delete_images'),
	url(r'^view_all_images/$',views.view_all_images,name='view_all_images'),
	url(r'^pull_images/(?P<name>\S+)/$',views.pull_images,name='pull_images'),
	url(r'^ask_create_container/$',views.ask_create_container,name='ask_create_container'),
	url(r'^create_container/(?P<image>\S+)/(?P<cmd>\S+)/(?P<cont_id>\S+)/$',views.create_container,name='create_container'),
	url(r'^view_all_containers/$',views.view_all_containers,name='view_all_containers'),
	url(r'^view_your_images/$',views.view_your_images,name='view_your_images'),
	url(r'^commit_container/(?P<container_id>\S+)/(?P<msg>\S+)/(?P<repo>\S+)$',views.commit_container,name='commit_container'),
	url(r'^view_your_containers/$',views.view_your_containers,name='view_your_containers'),
	url(r'^ask_push_images1/$',views.ask_push_images1,name='ask_push_images1'),
	url(r'^ask_push_images2/$',views.ask_push_images2,name='ask_push_images2'),
	url(r'^ask_push_images3/$',views.ask_push_images3,name='ask_push_images3'),
	url(r'^push_images/(?P<img_name>\S+)/$',views.push_images,name='push_images'),
	#url(r'^/$',views.view_request_thanks,name='view_request_thanks'),
]