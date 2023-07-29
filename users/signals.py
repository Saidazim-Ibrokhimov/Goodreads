# from django.dispatch import receiver 
# from django.db.models.signals import post_save
# from users.models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def send_welcome(sender, instance, created, **kwargs):
# 	if created:
# 		print('Created')
# 	else:
# 		print("Changed")