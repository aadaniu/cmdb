"""cmdb_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from opmanage.views import index, test, test_zabbix

urlpatterns = [
    url(r'^test/adduesr', test.insert_data),
    url(r'^test/sendtable', test.sendtable),
    url(r'^test/sendmail', test.send),
    url(r'^test/zabbix', test_zabbix.test_zabbix),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', index.login),
    url(r'^logout/', index.logout),
    url(r'^adduser/', index.add_user),
    url(r'^deluser/', index.del_user),
    url(r'^index/', index.del_user),
    url(r'^changepassword/',index.change_password),
    url(r'^changeuserinfo/',index.change_user_info),
]

