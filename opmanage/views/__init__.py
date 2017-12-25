from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_delete, post_delete
from django.db.models.signals import m2m_changed


from opmanage.models import Host_info
from opmanage.views.host import del_zabbix_host


# http://python.usyiyi.cn/documents/Django_111/ref/signals.html

@receiver(post_delete, sender=Host_info)
def delhost_callback(sender, instance, **kwargs):
    print '1111'
    print instance.host_name


