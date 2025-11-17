from rest_framework import routers
from .viewsets import HouseViewset
app_name="house"
router=routers.DefaultRouter()
router.register('houses',HouseViewset)